import asyncio
import io
from typing import Any, List
from uuid import UUID

from fastapi import UploadFile
from quivr_core.models import KnowledgeStatus
from sqlalchemy.exc import NoResultFound

from quivr_api.logger import get_logger
from quivr_api.modules.dependencies import BaseService
from quivr_api.modules.knowledge.dto.inputs import (
    AddKnowledge,
    CreateKnowledgeProperties,
)
from quivr_api.modules.knowledge.dto.outputs import DeleteKnowledgeResponse
from quivr_api.modules.knowledge.entity.knowledge import (
    Knowledge,
    KnowledgeDB,
    KnowledgeSource,
    KnowledgeUpdate,
)
from quivr_api.modules.knowledge.repository.knowledges import KnowledgeRepository
from quivr_api.modules.knowledge.repository.storage import SupabaseS3Storage
from quivr_api.modules.knowledge.repository.storage_interface import StorageInterface
from quivr_api.modules.knowledge.service.knowledge_exceptions import (
    KnowledgeDeleteError,
    KnowledgeForbiddenAccess,
    UploadError,
)
from quivr_api.modules.sync.entity.sync_models import (
    DBSyncFile,
    DownloadedSyncFile,
    SyncFile,
)
from quivr_api.modules.upload.service.upload_file import check_file_exists

logger = get_logger(__name__)


class KnowledgeService(BaseService[KnowledgeRepository]):
    repository_cls = KnowledgeRepository

    def __init__(
        self,
        repository: KnowledgeRepository,
        storage: StorageInterface = SupabaseS3Storage(),
    ):
        self.repository = repository
        self.storage = storage

    async def get_knowledge_sync(self, sync_id: int) -> Knowledge:
        km_db = await self.repository.get_knowledge_by_sync_id(sync_id)
        assert km_db.id, "Knowledge ID not generated"
        km = await km_db.to_dto()
        return km

    # TODO: this is temporary fix for getting knowledge path.
    # KM storage path should be unrelated to brain
    async def get_knowledge_storage_path(
        self, file_name: str, brain_id: UUID
    ) -> str | None:
        try:
            km = await self.repository.get_knowledge_by_file_name_brain_id(
                file_name, brain_id
            )
            brains = await km.awaitable_attrs.brains
            return next(
                f"{b.brain_id}/{file_name}"
                for b in brains
                if check_file_exists(str(b.brain_id), file_name)
            )
        except NoResultFound:
            raise FileNotFoundError(f"No knowledge for file_name: {file_name}")

    async def list_knowledge(
        self, knowledge_id: UUID | None, user_id: UUID | None = None
    ) -> list[KnowledgeDB]:
        if knowledge_id is not None:
            km = await self.repository.get_knowledge_by_id(knowledge_id, user_id)
            return km.children
        else:
            if user_id is None:
                raise KnowledgeForbiddenAccess(
                    "can't get root knowledges without user_id"
                )
            return await self.repository.get_root_knowledge_user(user_id)

    async def get_knowledge(
        self, knowledge_id: UUID, user_id: UUID | None = None
    ) -> KnowledgeDB:
        return await self.repository.get_knowledge_by_id(knowledge_id, user_id)

    async def update_knowledge(
        self,
        knowledge: KnowledgeDB,
        payload: Knowledge | KnowledgeUpdate | dict[str, Any],
    ):
        return await self.repository.update_knowledge(knowledge, payload)

    # TODO: Remove all of this
    # TODO (@aminediro): Replace with ON CONFLICT smarter query...
    # there is a chance of race condition but for now we let it crash in worker
    # the tasks will be dealt with on retry
    async def update_sha1_conflict(
        self, knowledge: KnowledgeDB, brain_id: UUID, file_sha1: str
    ) -> bool:
        assert knowledge.id
        knowledge.file_sha1 = file_sha1

        try:
            existing_knowledge = await self.repository.get_knowledge_by_sha1(
                knowledge.file_sha1
            )
            logger.debug("The content of the knowledge already exists in the brain. ")
            # Get existing knowledge sha1 and brains
            if (
                existing_knowledge.status == KnowledgeStatus.UPLOADED
                or existing_knowledge.status == KnowledgeStatus.PROCESSING
            ):
                existing_brains = await existing_knowledge.awaitable_attrs.brains
                if brain_id in [b.brain_id for b in existing_brains]:
                    logger.debug("Added file to brain that already has the knowledge")
                    raise FileExistsError(
                        f"Existing file in brain {brain_id} with name {existing_knowledge.file_name}"
                    )
                else:
                    await self.repository.link_to_brain(existing_knowledge, brain_id)
                    await self.remove_knowledge_brain(brain_id, knowledge.id)
                    return False
            else:
                logger.debug(f"Removing previous errored file {existing_knowledge.id}")
                assert existing_knowledge.id
                await self.remove_knowledge_brain(brain_id, existing_knowledge.id)
                await self.update_file_sha1_knowledge(knowledge.id, knowledge.file_sha1)
                return True
        except NoResultFound:
            logger.debug(
                f"First knowledge with sha1. Updating file_sha1 of  {knowledge.id}"
            )
            await self.update_file_sha1_knowledge(knowledge.id, knowledge.file_sha1)
            return True

    async def create_knowledge(
        self,
        user_id: UUID,
        knowledge_to_add: AddKnowledge,
        upload_file: UploadFile | None = None,
    ) -> KnowledgeDB:
        knowledgedb = KnowledgeDB(
            user_id=user_id,
            file_name=knowledge_to_add.file_name,
            is_folder=knowledge_to_add.is_folder,
            url=knowledge_to_add.url,
            extension=knowledge_to_add.extension,
            source=knowledge_to_add.source,
            source_link=knowledge_to_add.source_link,
            file_size=upload_file.size if upload_file else 0,
            metadata_=knowledge_to_add.metadata,  # type: ignore
            status=KnowledgeStatus.RESERVED,
            parent_id=knowledge_to_add.parent_id,
        )
        knowledge_db = await self.repository.create_knowledge(knowledgedb)
        try:
            if knowledgedb.source == KnowledgeSource.LOCAL and upload_file:
                # NOTE(@aminediro): Unnecessary mem buffer because supabase doesnt accept FileIO..
                buff_reader = io.BufferedReader(upload_file.file)  # type: ignore
                storage_path = await self.storage.upload_file_storage(
                    knowledgedb, buff_reader
                )
                knowledgedb.source_link = storage_path
            knowledge_db = await self.repository.update_knowledge(
                knowledge_db,
                KnowledgeUpdate(status=KnowledgeStatus.UPLOADED),  # type: ignore
            )
            return knowledge_db
        except Exception as e:
            logger.exception(
                f"Error uploading knowledge {knowledgedb.id} to storage : {e}"
            )
            await self.repository.remove_knowledge(knowledge=knowledge_db)
            raise UploadError()

    async def insert_knowledge_brain(
        self,
        user_id: UUID,
        knowledge_to_add: CreateKnowledgeProperties,  # FIXME: (later) @Amine brain id should not be in CreateKnowledgeProperties but since storage is brain_id/file_name
    ) -> Knowledge:
        knowledge = KnowledgeDB(
            file_name=knowledge_to_add.file_name,
            url=knowledge_to_add.url,
            extension=knowledge_to_add.extension,
            status=knowledge_to_add.status.value,
            source=knowledge_to_add.source,
            source_link=knowledge_to_add.source_link,
            file_size=knowledge_to_add.file_size,
            file_sha1=knowledge_to_add.file_sha1,
            metadata_=knowledge_to_add.metadata,  # type: ignore
            user_id=user_id,
        )

        knowledge_db = await self.repository.insert_knowledge_brain(
            knowledge, brain_id=knowledge_to_add.brain_id
        )

        assert knowledge_db.id, "Knowledge ID not generated"
        inserted_knowledge = await knowledge_db.to_dto()
        return inserted_knowledge

    async def get_all_knowledge_in_brain(self, brain_id: UUID) -> List[Knowledge]:
        brain = await self.repository.get_brain_by_id(brain_id, get_knowledge=True)
        all_knowledges: List[KnowledgeDB] = await brain.awaitable_attrs.knowledges
        knowledges = [
            await knowledge.to_dto(get_children=False, get_parent=False)
            for knowledge in all_knowledges
        ]

        return knowledges

    async def update_status_knowledge(
        self,
        knowledge_id: UUID,
        status: KnowledgeStatus,
        brain_id: UUID | None = None,
    ):
        knowledge = await self.repository.update_status_knowledge(knowledge_id, status)
        assert knowledge, "Knowledge not found"
        if status == KnowledgeStatus.ERROR and brain_id:
            assert isinstance(knowledge.file_name, str), "file_name should be a string"
            file_name_with_brain_id = f"{brain_id}/{knowledge.file_name}"
            try:
                await self.storage.remove_file(file_name_with_brain_id)
            except Exception as e:
                logger.error(
                    f"Error while removing file {file_name_with_brain_id}: {e}"
                )

        return knowledge

    async def update_file_sha1_knowledge(self, knowledge_id: UUID, file_sha1: str):
        return await self.repository.update_file_sha1_knowledge(knowledge_id, file_sha1)

    async def remove_knowledge(self, knowledge: KnowledgeDB) -> DeleteKnowledgeResponse:
        assert knowledge.id

        try:
            # TODO:
            # - Notion folders are special, they are themselves files and should be removed from storage
            children = await self.repository.get_all_children(knowledge.id)
            km_paths = [
                self.storage.get_storage_path(k) for k in children if not k.is_folder
            ]
            if not knowledge.is_folder:
                km_paths.append(self.storage.get_storage_path(knowledge))

            # recursively deletes files
            deleted_km = await self.repository.remove_knowledge(knowledge)
            await asyncio.gather(*[self.storage.remove_file(p) for p in km_paths])

            return deleted_km
        except Exception as e:
            logger.error(f"Error while remove knowledge : {e}")
            raise KnowledgeDeleteError

    async def remove_knowledge_brain(
        self,
        brain_id: UUID,
        knowledge_id: UUID,  # FIXME: @amine when name in storage change no need for brain id
    ) -> DeleteKnowledgeResponse:
        # TODO: fix KMS
        # REDO ALL THIS
        knowledge = await self.repository.get_knowledge_by_id(knowledge_id)
        km_brains = await knowledge.awaitable_attrs.brains
        if len(km_brains) > 1:
            km = await self.repository.remove_knowledge_from_brain(
                knowledge_id, brain_id
            )
            assert km.id
            return DeleteKnowledgeResponse(file_name=km.file_name, knowledge_id=km.id)
        else:
            message = await self.repository.remove_knowledge_by_id(knowledge_id)
            file_name_with_brain_id = f"{brain_id}/{message.file_name}"
            try:
                await self.storage.remove_file(file_name_with_brain_id)
            except Exception as e:
                logger.error(
                    f"Error while removing file {file_name_with_brain_id}: {e}"
                )
            return message

    async def remove_all_knowledges_from_brain(self, brain_id: UUID) -> None:
        await self.repository.remove_all_knowledges_from_brain(brain_id)

        logger.info(
            f"All knowledge in brain {brain_id} removed successfully from table"
        )

    # TODO: REDO THIS MESS !!!!
    # REMOVE ALL SYNC TABLES and start from scratch
    async def update_or_create_knowledge_sync(
        self,
        brain_id: UUID,
        user_id: UUID,
        file: SyncFile,
        new_sync_file: DBSyncFile | None,
        prev_sync_file: DBSyncFile | None,
        downloaded_file: DownloadedSyncFile,
        source: str,
        source_link: str,
    ) -> Knowledge:
        sync_id = None
        # TODO: THIS IS A HACK!! Remove all of this
        if prev_sync_file:
            prev_knowledge = await self.get_knowledge_sync(sync_id=prev_sync_file.id)
            if len(prev_knowledge.brains) > 1:
                await self.repository.remove_knowledge_from_brain(
                    prev_knowledge.id, brain_id
                )
            else:
                await self.repository.remove_knowledge_by_id(prev_knowledge.id)
            sync_id = prev_sync_file.id

        sync_id = new_sync_file.id if new_sync_file else sync_id
        knowledge_to_add = CreateKnowledgeProperties(
            brain_id=brain_id,
            file_name=file.name,
            extension=downloaded_file.extension,
            source=source,
            status=KnowledgeStatus.PROCESSING,
            source_link=source_link,
            file_size=file.size if file.size else 0,
            # FIXME (@aminediro): This is a temporary fix, redo in KMS
            file_sha1=None,
            metadata={"sync_file_id": str(sync_id)},
        )
        added_knowledge = await self.insert_knowledge_brain(
            knowledge_to_add=knowledge_to_add, user_id=user_id
        )
        return added_knowledge
