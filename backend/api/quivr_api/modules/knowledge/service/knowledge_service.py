from typing import List
from uuid import UUID

from quivr_core.models import KnowledgeStatus
from sqlalchemy.exc import IntegrityError

from quivr_api.logger import get_logger
from quivr_api.modules.dependencies import BaseService
from quivr_api.modules.knowledge.dto.inputs import (
    CreateKnowledgeProperties,
)
from quivr_api.modules.knowledge.dto.outputs import DeleteKnowledgeResponse
from quivr_api.modules.knowledge.entity.knowledge import Knowledge, KnowledgeDB
from quivr_api.modules.knowledge.repository.knowledges import KnowledgeRepository
from quivr_api.modules.knowledge.repository.storage import Storage

logger = get_logger(__name__)


class KnowledgeService(BaseService[KnowledgeRepository]):
    repository_cls = KnowledgeRepository

    def __init__(self, repository: KnowledgeRepository):
        self.repository = repository
        self.storage = Storage()

    async def get_knowledge_sync(self, sync_id: int) -> Knowledge:
        km = await self.repository.get_knowledge_by_sync_id(sync_id)
        assert km.id, "Knowledge ID not generated"
        km = await km.to_dto()
        return km

    async def get_knowledge(self, knowledge_id: UUID) -> Knowledge:
        inserted_knowledge_db_instance = await self.repository.get_knowledge_by_id(
            knowledge_id
        )
        assert inserted_knowledge_db_instance.id, "Knowledge ID not generated"
        km = await inserted_knowledge_db_instance.to_dto()
        return km

    async def insert_knowledge(
        self,
        knowledge_to_add: CreateKnowledgeProperties,  # FIXME: (later) @Amine brain id should not be in CreateKnowledgeProperties but since storage is brain_id/file_name
    ) -> Knowledge:
        knowledge = KnowledgeDB(
            file_name=knowledge_to_add.file_name,
            url=knowledge_to_add.url,
            mime_type=knowledge_to_add.mime_type,
            status=knowledge_to_add.status.value,
            source=knowledge_to_add.source,
            source_link=knowledge_to_add.source_link,
            file_size=knowledge_to_add.file_size,
            file_sha1=knowledge_to_add.file_sha1,
            metadata_=knowledge_to_add.metadata,  # type: ignore
        )

        knowledge_db = await self.repository.insert_knowledge(
            knowledge, brain_id=knowledge_to_add.brain_id
        )

        assert knowledge_db.id, "Knowledge ID not generated"
        inserted_knowledge = await knowledge_db.to_dto()
        return inserted_knowledge

    async def get_all_knowledge(self, brain_id: UUID) -> List[Knowledge]:
        brain = await self.repository.get_brain_by_id(brain_id)

        all_knowledges = await brain.awaitable_attrs.knowledges
        knowledges = [await knowledge.to_dto() for knowledge in all_knowledges]

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
                self.storage.remove_file(file_name_with_brain_id)
            except Exception as e:
                logger.error(
                    f"Error while removing file {file_name_with_brain_id}: {e}"
                )

        return knowledge

    async def update_file_sha1_knowledge(self, knowledge_id: UUID, file_sha1: str):
        try:
            knowledge = await self.repository.update_file_sha1_knowledge(
                knowledge_id, file_sha1
            )

            return knowledge
        except IntegrityError:
            raise FileExistsError(
                f"File {knowledge_id} already exists maybe under another file_name"
            )

    async def remove_knowledge(
        self,
        brain_id: UUID,
        knowledge_id: UUID,  # FIXME: @amine when name in storage change no need for brain id
    ) -> DeleteKnowledgeResponse:
        message = await self.repository.remove_knowledge_by_id(knowledge_id)
        file_name_with_brain_id = f"{brain_id}/{message.file_name}"
        try:
            self.storage.remove_file(file_name_with_brain_id)
        except Exception as e:
            logger.error(f"Error while removing file {file_name_with_brain_id}: {e}")

        return message

    async def remove_brain_all_knowledge(self, brain_id: UUID) -> None:
        await self.repository.remove_brain_all_knowledge(brain_id)

        logger.info(
            f"All knowledge in brain {brain_id} removed successfully from table"
        )
