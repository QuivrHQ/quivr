import asyncio
import io
from datetime import datetime
from typing import Any, List
from uuid import UUID

from fastapi import UploadFile
from quivr_core.models import KnowledgeStatus
from sqlalchemy.exc import NoResultFound

from quivr_api.celery_config import celery
from quivr_api.logger import get_logger
from quivr_api.modules.brain.entity.brain_entity import Brain
from quivr_api.modules.dependencies import BaseService
from quivr_api.modules.knowledge.dto.inputs import (
    AddKnowledge,
    CreateKnowledgeProperties,
    KnowledgeUpdate,
)
from quivr_api.modules.knowledge.dto.outputs import (
    DeleteKnowledgeResponse,
    KnowledgeDTO,
)
from quivr_api.modules.knowledge.entity.knowledge import (
    KnowledgeDB,
    KnowledgeSource,
)
from quivr_api.modules.knowledge.repository.knowledges import KnowledgeRepository
from quivr_api.modules.knowledge.repository.storage import SupabaseS3Storage
from quivr_api.modules.knowledge.repository.storage_interface import StorageInterface
from quivr_api.modules.knowledge.service.knowledge_exceptions import (
    KnowledgeDeleteError,
    KnowledgeForbiddenAccess,
    UploadError,
)
from quivr_api.modules.sync.entity.sync_models import SyncFile, SyncType
from quivr_api.modules.upload.service.upload_file import check_file_exists

logger = get_logger(__name__)


class KnowledgeService(BaseService[KnowledgeRepository]):
    repository_cls = KnowledgeRepository

    def __init__(
        self,
        repository: KnowledgeRepository,
        storage: StorageInterface = SupabaseS3Storage(client=None),
    ):
        self.repository = repository
        self.storage = storage

    async def get_knowledge_sync(self, sync_id: int) -> KnowledgeDTO:
        km = await self.repository.get_knowledge_by_sync_id(sync_id)
        assert km.id, "Knowledge ID not generated"
        km = await km.to_dto()
        return km

    async def create_or_link_sync_knowledge(
        self,
        syncfile_id_to_knowledge: dict[str, KnowledgeDB],
        parent_knowledge: KnowledgeDB,
        sync_file: SyncFile,
        autocommit: bool = True,
    ):
        existing_km = syncfile_id_to_knowledge.get(sync_file.id)
        if existing_km is not None:
            # NOTE: function called in worker processor
            # The parent_knowledge was just added to db (we are processing it)
            # This implies that we could have sync children files and folders that were processed before
            # If SyncKnowledge already exists
            #   IF STATUS == PROCESSED:
            #   => It's already processed in some other brain !
            #   => Link it to the parent and update its brains to the correct ones
            #   ELSE Reprocess the file
            km_brains = {km_brain.brain_id for km_brain in existing_km.brains}
            for brain in filter(
                lambda b: b.brain_id not in km_brains,
                parent_knowledge.brains,
            ):
                await self.repository.update_knowledge(
                    existing_km,
                    KnowledgeUpdate(parent_id=parent_knowledge.id),
                    autocommit=autocommit,
                )
                await self.repository.link_to_brain(
                    existing_km, brain_id=brain.brain_id
                )
            return existing_km
        else:
            # create sync file knowledge
            # automagically gets the brains associated with the parent
            file_knowledge = await self.create_knowledge(
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
            return file_knowledge

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

    async def map_syncs_knowledge_user(
        self, sync_id: int, user_id: UUID
    ) -> dict[str, KnowledgeDB]:
        list_kms = await self.repository.get_all_knowledge_sync_user(
            sync_id=sync_id, user_id=user_id
        )
        return {k.sync_file_id: k for k in list_kms if k.sync_file_id}

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
        knowledge: KnowledgeDB | UUID,
        payload: KnowledgeDTO | KnowledgeUpdate | dict[str, Any],
        autocommit: bool = True,
    ):
        if isinstance(knowledge, UUID):
            knowledge = await self.repository.get_knowledge_by_id(knowledge)
        return await self.repository.update_knowledge(knowledge, payload, autocommit)

    async def create_knowledge(
        self,
        user_id: UUID,
        knowledge_to_add: AddKnowledge,
        upload_file: UploadFile | None = None,
        status: KnowledgeStatus = KnowledgeStatus.RESERVED,
        add_brains: list[Brain] = [],
        autocommit: bool = True,
    ) -> KnowledgeDB:
        brains = []
        if knowledge_to_add.parent_id:
            parent_knowledge = await self.get_knowledge(knowledge_to_add.parent_id)
            brains = await parent_knowledge.awaitable_attrs.brains
        if len(add_brains) > 0:
            brains.extend(
                [
                    b
                    for b in add_brains
                    if b.brain_id not in {b.brain_id for b in brains}
                ]
            )

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
            status=status,
            parent_id=knowledge_to_add.parent_id,
            sync_id=knowledge_to_add.sync_id,
            sync_file_id=knowledge_to_add.sync_file_id,
            brains=brains,
        )

        knowledge_db = await self.repository.create_knowledge(
            knowledgedb, autocommit=autocommit
        )

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
                    KnowledgeUpdate(status=KnowledgeStatus.UPLOADED),
                    autocommit=autocommit,
                )
            if knowledge_db.brains and len(knowledge_db.brains) > 0:
                # Schedule this new knowledge to be processed
                knowledge_db = await self.repository.update_knowledge(
                    knowledge_db,
                    KnowledgeUpdate(status=KnowledgeStatus.PROCESSING),
                    autocommit=autocommit,
                )
                celery.send_task(
                    "process_file_task",
                    kwargs={
                        "knowledge_id": knowledge_db.id,
                    },
                )

            return knowledge_db
        except Exception as e:
            logger.exception(
                f"Error uploading knowledge {knowledgedb.id} to storage : {e}"
            )
            await self.repository.remove_knowledge(
                knowledge=knowledge_db, autocommit=autocommit
            )
            raise UploadError()

    async def insert_knowledge_brain(
        self,
        user_id: UUID,
        knowledge_to_add: CreateKnowledgeProperties,  # FIXME: (later) @Amine brain id should not be in CreateKnowledgeProperties but since storage is brain_id/file_name
    ) -> KnowledgeDTO:
        # TODO: check input
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

    async def get_all_knowledge_in_brain(self, brain_id: UUID) -> List[KnowledgeDTO]:
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

    async def remove_knowledge(
        self, knowledge: KnowledgeDB, autocommit: bool = True
    ) -> DeleteKnowledgeResponse:
        assert knowledge.id

        try:
            # TODO:
            # - Notion folders are special, they are themselves files and should be removed from storage
            km_paths = []
            if knowledge.source == KnowledgeSource.LOCAL:
                if knowledge.is_folder:
                    children = await self.repository.get_knowledge_tree(knowledge.id)
                    km_paths.extend(
                        [
                            self.storage.get_storage_path(k)
                            for k in children
                            if not k.is_folder
                        ]
                    )
                if not knowledge.is_folder:
                    km_paths.append(self.storage.get_storage_path(knowledge))
            # recursively deletes files
            deleted_km = await self.repository.remove_knowledge(
                knowledge, autocommit=autocommit
            )
            # TODO: remove storage asynchronously in background task or in some task
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

    async def link_knowledge_tree_brains(
        self, knowledge: KnowledgeDB | UUID, brains_ids: List[UUID], user_id: UUID
    ) -> List[KnowledgeDB]:
        if isinstance(knowledge, UUID):
            knowledge = await self.repository.get_knowledge_by_id(knowledge)
        return await self.repository.link_knowledge_tree_brains(
            knowledge, brains_ids=brains_ids, user_id=user_id
        )

    async def unlink_knowledge_tree_brains(
        self, knowledge: KnowledgeDB | UUID, brains_ids: List[UUID], user_id: UUID
    ) -> List[KnowledgeDB] | None:
        if isinstance(knowledge, UUID):
            knowledge = await self.repository.get_knowledge_by_id(knowledge)
        return await self.repository.unlink_knowledge_tree_brains(
            knowledge, brains_ids=brains_ids, user_id=user_id
        )

    async def get_outdated_syncs(
        self,
        limit_time: datetime,
        km_sync_type: SyncType,
        batch_size: int = 1,
    ) -> List[KnowledgeDB]:
        return await self.repository.get_outdated_syncs(
            limit_time=limit_time, batch_size=batch_size, km_sync_type=km_sync_type
        )
