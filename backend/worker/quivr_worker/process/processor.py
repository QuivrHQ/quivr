from contextlib import asynccontextmanager
from dataclasses import dataclass
from io import BytesIO
from typing import Any, AsyncGenerator, List, Optional, Tuple
from uuid import UUID

from quivr_api.logger import get_logger
from quivr_api.modules.dependencies import get_supabase_async_client
from quivr_api.modules.knowledge.dto.inputs import AddKnowledge, KnowledgeUpdate
from quivr_api.modules.knowledge.dto.outputs import KnowledgeDTO
from quivr_api.modules.knowledge.entity.knowledge import KnowledgeDB, KnowledgeSource
from quivr_api.modules.knowledge.repository.knowledges import KnowledgeRepository
from quivr_api.modules.knowledge.repository.storage import SupabaseS3Storage
from quivr_api.modules.knowledge.service.knowledge_service import KnowledgeService
from quivr_api.modules.sync.dto.outputs import SyncProvider
from quivr_api.modules.sync.entity.sync_models import SyncFile
from quivr_api.modules.sync.repository.sync_repository import SyncsRepository
from quivr_api.modules.sync.service.sync_service import SyncsService
from quivr_api.modules.sync.utils.sync import (
    BaseSync,
)
from quivr_api.modules.vector.repository.vectors_repository import VectorRepository
from quivr_api.modules.vector.service.vector_service import VectorService
from quivr_core.files.file import QuivrFile
from quivr_core.models import KnowledgeStatus
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import text
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_worker.process.process_file import parse_qfile, store_chunks
from quivr_worker.process.utils import (
    build_qfile,
    build_syncprovider_mapping,
    compute_sha1,
    skip_process,
)

logger = get_logger("celery_worker")


@dataclass
class ProcessorServices:
    sync_service: SyncsService
    vector_service: VectorService
    knowledge_service: KnowledgeService
    syncprovider_mapping: dict[SyncProvider, BaseSync]


@asynccontextmanager
async def _start_session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        try:
            await session.execute(
                text("SET SESSION idle_in_transaction_session_timeout = '5min';")
            )
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


@asynccontextmanager
async def build_processor_services(engine: AsyncEngine):
    async_client = await get_supabase_async_client()
    storage = SupabaseS3Storage(async_client)
    try:
        async with _start_session(engine) as session:
            vector_repository = VectorRepository(session)
            vector_service = VectorService(vector_repository)
            knowledge_repository = KnowledgeRepository(session)
            knowledge_service = KnowledgeService(knowledge_repository, storage=storage)
            sync_repository = SyncsRepository(session)
            sync_service = SyncsService(sync_repository)
            yield ProcessorServices(
                knowledge_service=knowledge_service,
                vector_service=vector_service,
                sync_service=sync_service,
                syncprovider_mapping=build_syncprovider_mapping(),
            )
    finally:
        logger.info("Closing processor services")


async def download_sync_file(
    sync_provider: BaseSync, file: SyncFile, credentials: dict[str, Any]
) -> bytes:
    logger.info(f"Downloading {file} using {sync_provider}")
    file_response = await sync_provider.adownload_file(credentials, file)
    logger.debug(f"Fetch sync file response: {file_response}")
    raw_data = file_response["content"]
    if isinstance(raw_data, BytesIO):
        file_data = raw_data.read()
    else:
        file_data = raw_data.encode("utf-8")
    logger.debug(f"Successfully downloaded sync file : {file}")
    return file_data


class KnowledgeProcessor:
    def __init__(self, services: ProcessorServices):
        self.services = services

    async def fetch_sync_knowledge(
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

    async def yield_processable_kms(
        self, knowledge: KnowledgeDTO
    ) -> AsyncGenerator[Tuple[KnowledgeDB, QuivrFile] | None, None]:
        if knowledge.source == KnowledgeSource.LOCAL:
            async for to_process in self._build_local(knowledge):
                yield to_process
        elif knowledge.source in (
            KnowledgeSource.AZURE,
            KnowledgeSource.GITHUB,
            KnowledgeSource.GOOGLE,
            KnowledgeSource.NOTION,
        ):
            async for to_process in self._build_sync(knowledge):
                yield to_process
        elif knowledge.source == KnowledgeSource.WEB:
            raise NotImplementedError
        else:
            logger.error(
                f"received knowledge : {knowledge.id} with unknown source: {knowledge.source}"
            )
            raise ValueError("Unknown knowledge source : {knoledge.source}")

    async def _build_local(
        self, knowledge: KnowledgeDTO
    ) -> AsyncGenerator[Tuple[KnowledgeDB, QuivrFile] | None, None]:
        if knowledge.id is None or knowledge.file_name is None:
            logger.error(f"received unprocessable local knowledge : {knowledge.id} ")
            raise ValueError(
                f"received unprocessable local knowledge : {knowledge.id} "
            )
        knowledge_db = await self.services.knowledge_service.get_knowledge(knowledge.id)
        file_data = await self.services.knowledge_service.storage.download_file(
            knowledge_db
        )
        knowledge_db.file_sha1 = compute_sha1(file_data)
        with build_qfile(knowledge_db, file_data) as qfile:
            yield (knowledge_db, qfile)

    async def _build_sync(
        self, knowledge_dto: KnowledgeDTO
    ) -> AsyncGenerator[Optional[Tuple[KnowledgeDB, QuivrFile]], None]:
        if knowledge_dto.id is None:
            logger.error(f"received unprocessable knowledge: {knowledge_dto.id} ")
            raise ValueError

        parent_knowledge = await self.services.knowledge_service.get_knowledge(
            knowledge_dto.id
        )
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
        sync = await self.services.sync_service.get_sync_by_id(parent_knowledge.sync_id)
        if sync.credentials is None:
            logger.error(f"can't process sync file. sync {sync.id} has no credentials")
            return
        provider_name = SyncProvider(sync.provider.lower())
        sync_provider = self.services.syncprovider_mapping[provider_name]

        syncfile_to_knowledge, sync_files = await self.fetch_sync_knowledge(
            sync_id=parent_knowledge.sync_id,
            user_id=parent_knowledge.user_id,
            folder_id=parent_knowledge.sync_file_id,
        )
        if not sync_files:
            return

        # Yield parent_knowledge as the first knowledge to process
        file_data = await download_sync_file(
            sync_provider=sync_provider,
            file=SyncFile(
                id=parent_knowledge.sync_file_id,
                name=parent_knowledge.file_name,
                extension=parent_knowledge.extension,
                web_view_link=parent_knowledge.source_link,
                is_folder=parent_knowledge.is_folder,
                last_modified_at=parent_knowledge.updated_at,
            ),
            credentials=sync.credentials,
        )
        parent_knowledge.file_sha1 = compute_sha1(file_data)
        with build_qfile(parent_knowledge, file_data) as qfile:
            yield (parent_knowledge, qfile)

        for sync_file in sync_files:
            existing_km = syncfile_to_knowledge.get(sync_file.id)
            if existing_km:
                file_knowledge = existing_km
            else:
                # create sync file knowledge
                # automagically gets the brains associated with the parent
                file_knowledge = await self.services.knowledge_service.create_knowledge(
                    user_id=parent_knowledge.user_id,
                    knowledge_to_add=AddKnowledge(
                        file_name=sync_file.name,
                        is_folder=sync_file.is_folder,
                        extension=sync_file.extension,
                        source=parent_knowledge.source,  # same as parent
                        source_link=sync_file.web_view_link,
                        parent_id=parent_knowledge.id,
                        sync_id=parent_knowledge.sync_id,
                        sync_file_id=sync_file.id,
                    ),
                    status=KnowledgeStatus.PROCESSING,
                    upload_file=None,
                )
            file_data = await download_sync_file(
                sync_provider=sync_provider,
                file=sync_file,
                credentials=sync.credentials,
            )
            file_knowledge.file_sha1 = compute_sha1(file_data)
            with build_qfile(file_knowledge, file_data) as qfile:
                yield (file_knowledge, qfile)

    async def process_knowledge(self, knowledge_dto: KnowledgeDTO):
        async for knowledge_tuple in self.yield_processable_kms(knowledge_dto):
            if knowledge_tuple is None:
                continue
            knowledge, qfile = knowledge_tuple
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
                    status=KnowledgeStatus.PROCESSED, file_sha1=knowledge.file_sha1
                ),
            )
