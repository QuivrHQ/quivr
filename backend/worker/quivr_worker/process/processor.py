import asyncio
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any, AsyncGenerator, List, Optional, Tuple
from uuid import UUID

from quivr_api.logger import get_logger
from quivr_api.modules.knowledge.dto.inputs import AddKnowledge, KnowledgeUpdate
from quivr_api.modules.knowledge.entity.knowledge import KnowledgeDB, KnowledgeSource
from quivr_api.modules.sync.dto.outputs import SyncProvider
from quivr_api.modules.sync.entity.sync_models import Sync, SyncFile, SyncType
from quivr_api.modules.sync.utils.sync import BaseSync
from quivr_core.files.file import QuivrFile
from quivr_core.models import KnowledgeStatus
from sqlalchemy.ext.asyncio import AsyncSessionTransaction

from quivr_worker.parsers.crawler import URL, extract_from_url
from quivr_worker.process.process_file import parse_qfile, store_chunks
from quivr_worker.process.utils import (
    build_qfile,
    build_sync_file,
    compute_sha1,
    skip_process,
)
from quivr_worker.utils.services import ProcessorServices

logger = get_logger("celery_worker")


class KnowledgeProcessor:
    def __init__(self, services: ProcessorServices):
        self.services = services

    async def fetch_db_knowledges_and_syncprovider(
        self,
        sync_id: int,
        user_id: UUID,
        folder_id: str | None,
    ) -> Tuple[dict[str, KnowledgeDB], List[SyncFile] | None]:
        map_knowledges_task = self.services.knowledge_service.map_syncs_knowledge_user(
            sync_id=sync_id, user_id=user_id
        )
        sync_files_task = self.services.sync_service.get_files_folder_user_sync(
            sync_id,
            user_id,
            folder_id,
        )
        return await asyncio.gather(*[map_knowledges_task, sync_files_task])  # type: ignore  # noqa: F821

    async def yield_processable_knowledge(
        self, knowledge_id: UUID
    ) -> AsyncGenerator[Tuple[KnowledgeDB, QuivrFile] | None, None]:
        """Should only yield ready to process knowledges:
        Knowledge ready to process:
            - Is either Local or Sync
            - Is in a status: PROCESSING | ERROR
            - Has an associated QuivrFile that is parsable
        """
        knowledge = await self.services.knowledge_service.get_knowledge(knowledge_id)
        if knowledge.source == KnowledgeSource.LOCAL:
            async for to_process in self._yield_local(knowledge):
                yield to_process
        elif knowledge.source in (
            KnowledgeSource.AZURE,
            KnowledgeSource.GOOGLE,
            KnowledgeSource.DROPBOX,
            KnowledgeSource.GITHUB,
            # KnowledgeSource.NOTION,
        ):
            async for to_process in self._yield_syncs(knowledge):
                yield to_process
        elif knowledge.source == KnowledgeSource.WEB:
            async for to_process in self._yield_web(knowledge):
                yield to_process
        else:
            logger.error(
                f"received knowledge : {knowledge.id} with unknown source: {knowledge.source}"
            )
            raise ValueError(f"Unknown knowledge source : {knowledge.source}")

    async def _yield_local(
        self, knowledge: KnowledgeDB
    ) -> AsyncGenerator[Tuple[KnowledgeDB, QuivrFile] | None, None]:
        if knowledge.id is None or knowledge.file_name is None:
            logger.error(f"received unprocessable local knowledge : {knowledge.id} ")
            raise ValueError(
                f"received unprocessable local knowledge : {knowledge.id} "
            )
        if knowledge.is_folder:
            yield (
                knowledge,
                QuivrFile(
                    id=knowledge.id,
                    original_filename=knowledge.file_name,
                    file_extension=knowledge.extension,
                    file_sha1="",
                    path=Path(),
                ),
            )
        else:
            file_data = await self.services.knowledge_service.storage.download_file(
                knowledge
            )
            knowledge.file_sha1 = compute_sha1(file_data)
            with build_qfile(knowledge, file_data) as qfile:
                yield (knowledge, qfile)

    async def _yield_web(
        self, knowledge_db: KnowledgeDB
    ) -> AsyncGenerator[Tuple[KnowledgeDB, QuivrFile] | None, None]:
        if knowledge_db.id is None or knowledge_db.url is None:
            logger.error(f"received unprocessable web knowledge : {knowledge_db.id} ")
            raise ValueError(
                f"received unprocessable web knowledge : {knowledge_db.id} "
            )
        crawl_website = URL(url=knowledge_db.url)
        extracted_content = await extract_from_url(crawl_website)
        extracted_content_bytes = extracted_content.encode("utf-8")
        knowledge_db.file_sha1 = compute_sha1(extracted_content_bytes)
        knowledge_db.file_size = len(extracted_content_bytes)
        with build_qfile(knowledge_db, extracted_content_bytes) as qfile:
            yield (knowledge_db, qfile)

    async def _yield_syncs(
        self, parent_knowledge: KnowledgeDB
    ) -> AsyncGenerator[Optional[Tuple[KnowledgeDB, QuivrFile]], None]:
        if parent_knowledge.id is None:
            logger.error(f"received unprocessable knowledge: {parent_knowledge.id} ")
            raise ValueError

        if parent_knowledge.file_name is None:
            logger.error(f"received unprocessable knowledge : {parent_knowledge.id} ")
            raise ValueError(
                f"received unprocessable knowledge : {parent_knowledge.id} "
            )
        if (
            parent_knowledge.sync_file_id is None
            or parent_knowledge.sync_id is None
            or parent_knowledge.source_link is None
        ):
            logger.error(
                f"unprocessable  sync knowledge : {parent_knowledge.id}. no sync_file_id"
            )
            raise ValueError(
                f"received unprocessable knowledge : {parent_knowledge.id} "
            )
        # Get associated sync
        sync = await self._get_sync(parent_knowledge.sync_id)
        if sync.credentials is None:
            logger.error(
                f"can't process knowledge: {parent_knowledge.id}. sync {sync.id} has no credentials"
            )
            raise ValueError("no associated credentials")

        provider_name = SyncProvider(sync.provider.lower())
        sync_provider = self.services.syncprovider_mapping[provider_name]

        # Yield parent_knowledge as the first knowledge to process
        async with build_sync_file(
            file_knowledge=parent_knowledge,
            credentials=sync.credentials,
            sync_provider=sync_provider,
            sync_file=SyncFile(
                id=parent_knowledge.sync_file_id,
                name=parent_knowledge.file_name,
                extension=parent_knowledge.extension,
                web_view_link=parent_knowledge.source_link,
                is_folder=parent_knowledge.is_folder,
                last_modified_at=parent_knowledge.updated_at,
            ),
        ) as f:
            yield f

        # Fetch children
        (
            syncfile_to_knowledge,
            sync_files,
        ) = await self.fetch_db_knowledges_and_syncprovider(
            sync_id=parent_knowledge.sync_id,
            user_id=parent_knowledge.user_id,
            folder_id=parent_knowledge.sync_file_id,
        )
        if not sync_files:
            return

        for sync_file in sync_files:
            file_knowledge = (
                await self.services.knowledge_service.create_or_link_sync_knowledge(
                    syncfile_id_to_knowledge=syncfile_to_knowledge,
                    parent_knowledge=parent_knowledge,
                    sync_file=sync_file,
                )
            )
            if file_knowledge.status == KnowledgeStatus.PROCESSED:
                continue
            async with build_sync_file(
                file_knowledge=file_knowledge,
                credentials=sync.credentials,
                sync_provider=sync_provider,
                sync_file=sync_file,
            ) as f:
                yield f

    async def create_savepoint(self) -> AsyncSessionTransaction:
        savepoint = (
            await self.services.knowledge_service.repository.session.begin_nested()
        )
        return savepoint

    async def process_knowledge(self, knowledge_id: UUID):
        async for knowledge_tuple in self.yield_processable_knowledge(knowledge_id):
            # FIXME(@AmineDiro) : nested transaction for making
            savepoint = await self.create_savepoint()
            if knowledge_tuple is None:
                continue
            knowledge, qfile = knowledge_tuple
            try:
                await self._process_inner(knowledge=knowledge, qfile=qfile)
                await savepoint.commit()
            except Exception as e:
                await savepoint.rollback()
                logger.error(f"Error processing knowledge {knowledge_id} : {e}")
                # FIXME: This one can also fail if knowledge was deleted
                await self.services.knowledge_service.update_knowledge(
                    knowledge,
                    KnowledgeUpdate(
                        status=KnowledgeStatus.ERROR,
                    ),
                )

    async def _process_inner(self, knowledge: KnowledgeDB, qfile: QuivrFile):
        last_synced_at = datetime.now(timezone.utc)
        if not skip_process(knowledge):
            chunks = await parse_qfile(qfile=qfile)
            await store_chunks(
                knowledge=knowledge,
                chunks=chunks,
                vector_service=self.services.vector_service,
            )
        await self.services.knowledge_service.update_knowledge(
            knowledge,
            KnowledgeUpdate(
                status=KnowledgeStatus.PROCESSED,
                file_sha1=knowledge.file_sha1,
                # Update sync
                last_synced_at=last_synced_at if knowledge.sync_id else None,
            ),
            autocommit=False,
        )

    @lru_cache(maxsize=50)  # noqa: B019
    async def _get_sync(self, sync_id: int) -> Sync:
        sync = await self.services.sync_service.get_sync_by_id(sync_id)
        return sync

    async def refresh_sync_folders(
        self, timedelta_hour: int = 8, batch_size: int = 100
    ):
        last_time = datetime.now(timezone.utc) - timedelta(hours=timedelta_hour)
        km_sync_folders = await self.services.knowledge_service.get_outdated_syncs(
            limit_time=last_time,
            batch_size=batch_size,
            km_sync_type=SyncType.FOLDER,
        )
        for sync_folder_km in km_sync_folders:
            await self.refresh_sync_folder(sync_folder_km)

    async def refresh_sync_folder(self, folder_km: KnowledgeDB) -> KnowledgeDB:
        assert folder_km.sync_id, "can only update sync files with sync_id"
        assert folder_km.sync_file_id, "can only update sync files with sync_file_id "
        sync = await self._get_sync(folder_km.sync_id)
        if sync.credentials is None:
            logger.error(
                f"can't process knowledge: {folder_km.id}. sync {sync.id} has no credentials"
            )
            raise ValueError(f"no associated credentials with knowledge {folder_km}")
        provider_name = SyncProvider(sync.provider.lower())
        sync_provider = self.services.syncprovider_mapping[provider_name]
        km_children: List[KnowledgeDB] = await folder_km.awaitable_attrs.children
        sync_children = {c.sync_file_id for c in km_children}
        try:
            sync_files = await sync_provider.aget_files(
                credentials=sync.credentials,
                folder_id=folder_km.sync_file_id,
                recursive=False,
            )
            for sync_entry in filter(lambda s: s.id not in sync_children, sync_files):
                await self.add_new_sync_entry(folder=folder_km, sync_entry=sync_entry)

        except FileNotFoundError:
            logger.info(
                f"Knowledge {folder_km.id} not found in remote sync. Removing the folder"
            )
            await self.services.knowledge_service.remove_knowledge(
                folder_km, autocommit=True
            )
        except Exception:
            logger.exception(f"Exception occured processing folder: {folder_km.id}")
        finally:
            await self.services.knowledge_service.update_knowledge(
                knowledge=folder_km,
                payload=KnowledgeUpdate(last_synced_at=datetime.now(timezone.utc)),
            )
        return folder_km

    async def add_new_sync_entry(self, folder: KnowledgeDB, sync_entry: SyncFile):
        sync_km = await self.services.knowledge_service.create_knowledge(
            user_id=folder.user_id,
            knowledge_to_add=AddKnowledge(
                file_name=sync_entry.name,
                is_folder=sync_entry.is_folder,
                extension=sync_entry.extension,
                source=folder.source,
                source_link=sync_entry.web_view_link,
                parent_id=folder.id,
                sync_id=folder.sync_id,
                sync_file_id=sync_entry.id,
            ),
            status=KnowledgeStatus.PROCESSING,
            upload_file=None,
            autocommit=True,
            process_async=False,
        )
        async for processable_tuple in self._yield_syncs(sync_km):
            if processable_tuple is None:
                continue
            knowledge, qfile = processable_tuple
            savepoint = await self.create_savepoint()
            try:
                await self._process_inner(knowledge=knowledge, qfile=qfile)
                await savepoint.commit()
            except Exception:
                await savepoint.rollback()
                logger.exception(f"Error occured processing :{knowledge.id}")

    async def refresh_knowledge_sync_files(
        self, timedelta_hour: int = 8, batch_size: int = 1000
    ):
        last_time = datetime.now(timezone.utc) - timedelta(hours=timedelta_hour)
        km_sync_files = await self.services.knowledge_service.get_outdated_syncs(
            limit_time=last_time,
            batch_size=batch_size,
            km_sync_type=SyncType.FILE,
        )
        for old_km in km_sync_files:
            try:
                assert old_km.sync_id, "can only update sync files with sync_id"
                assert (
                    old_km.sync_file_id
                ), "can only update sync files with sync_file_id "
                sync = await self._get_sync(old_km.sync_id)
                if sync.credentials is None:
                    logger.error(
                        f"can't process knowledge: {old_km.id}. sync {sync.id} has no credentials"
                    )
                    raise ValueError(
                        f"no associated credentials with knowledge {old_km}"
                    )
                provider_name = SyncProvider(sync.provider.lower())
                sync_provider = self.services.syncprovider_mapping[provider_name]
                new_sync_file = (
                    await sync_provider.aget_files_by_id(
                        credentials=sync.credentials, file_ids=[old_km.sync_file_id]
                    )
                )[0]
                await self.refresh_knowledge_entry(
                    old_km=old_km,
                    new_sync_file=new_sync_file,
                    sync_provider=sync_provider,
                    sync_credentials=sync.credentials,
                )
            except FileNotFoundError:
                logger.info(
                    f"Knowledge {old_km.id} not found in remote sync. Removing the knowledge"
                )
                await self.services.knowledge_service.remove_knowledge(
                    old_km, autocommit=True
                )
            except Exception:
                logger.exception(f"Exception occured processing km: {old_km.id}")

    async def refresh_knowledge_entry(
        self,
        old_km: KnowledgeDB,
        new_sync_file: SyncFile,
        sync_provider: BaseSync,
        sync_credentials: dict[str, Any],
    ) -> KnowledgeDB | None:
        assert (
            old_km.last_synced_at
        ), "can only update sync files without a last_synced_at"
        if (
            new_sync_file.last_modified_at
            and new_sync_file.last_modified_at > old_km.last_synced_at
        ) or new_sync_file.last_modified_at is None:
            savepoint = await self.create_savepoint()
            try:
                new_km = await self.services.knowledge_service.create_knowledge(
                    user_id=old_km.user_id,
                    knowledge_to_add=AddKnowledge(
                        file_name=new_sync_file.name,
                        is_folder=new_sync_file.is_folder,
                        extension=new_sync_file.extension,
                        source=old_km.source,
                        source_link=new_sync_file.web_view_link,
                        parent_id=old_km.parent_id,
                        sync_id=old_km.sync_id,
                        sync_file_id=new_sync_file.id,
                    ),
                    status=KnowledgeStatus.PROCESSING,
                    link_brains=await old_km.awaitable_attrs.brains,
                    upload_file=None,
                    autocommit=False,
                    process_async=False,
                )
                async with build_sync_file(
                    new_km,
                    new_sync_file,
                    sync_provider=sync_provider,
                    credentials=sync_credentials,
                ) as (
                    new_km,
                    qfile,
                ):
                    await self._process_inner(new_km, qfile)
                await self.services.knowledge_service.remove_knowledge(
                    old_km, autocommit=False
                )
                await savepoint.commit()
                await savepoint.session.refresh(new_km)
                return new_km

            except Exception as e:
                logger.exception(
                    f"Rolling back. Error occured updating sync {old_km.id}: {e}"
                )
                await savepoint.rollback()
