from typing import List
from uuid import UUID

from quivr_api.logger import get_logger
from quivr_api.modules.dependencies import BaseService
from quivr_api.modules.knowledge.dto.inputs import (CreateKnowledgeProperties,
                                                    KnowledgeStatus)
from quivr_api.modules.knowledge.dto.outputs import DeleteKnowledgeResponse
from quivr_api.modules.knowledge.entity.knowledge import KnowledgeDB
from quivr_api.modules.knowledge.repository.knowledges import \
    KnowledgeRepository
from quivr_core.models import QuivrKnowledge as Knowledge
from sqlmodel.ext.asyncio.session import AsyncSession

logger = get_logger(__name__)


class KnowledgeService(BaseService[KnowledgeRepository]):
    repository: KnowledgeRepository

    def __init__(self, session: AsyncSession):
        self.repository = KnowledgeRepository(session)

    async def add_knowledge(self, knowledge_to_add: CreateKnowledgeProperties) -> Knowledge:
        knowledge_data = knowledge_to_add.dict()
        knowledge = KnowledgeDB(**knowledge_data)

        inserted_knowledge_db_instance = await self.repository.insert_knowledge(knowledge)

        assert inserted_knowledge_db_instance.id, "Knowledge ID not generated"

        inserted_knowledge = Knowledge(
        id= inserted_knowledge_db_instance.id,
        brain_id=inserted_knowledge_db_instance.brain_id,
        file_name=inserted_knowledge_db_instance.file_name,
        url=inserted_knowledge_db_instance.url,
        mime_type=inserted_knowledge_db_instance.mime_type,
        status=inserted_knowledge_db_instance.status,
        source=inserted_knowledge_db_instance.source,
        source_link=inserted_knowledge_db_instance.source_link,
        file_size=inserted_knowledge_db_instance.file_size,
        file_sha1=inserted_knowledge_db_instance.file_sha1,
        updated_at=inserted_knowledge_db_instance.updated_at,
        created_at=inserted_knowledge_db_instance.created_at,
        metadata=inserted_knowledge_db_instance.metadata # type: ignore
        )
        return inserted_knowledge

    async def get_all_knowledge(self, brain_id: UUID) -> List[Knowledge]:
        knowledges_models = await self.repository.get_all_knowledge_in_brain(brain_id)

        knowledges = [
            Knowledge(
                id=knowledge.id, # type: ignore
                brain_id=knowledge.brain_id,
                file_name=knowledge.file_name,
                url=knowledge.url,
                mime_type=knowledge.mime_type,
                status=knowledge.status,
                source=knowledge.source,
                source_link=knowledge.source_link,
                file_size=knowledge.file_size,
                file_sha1=knowledge.file_sha1,
                updated_at=knowledge.updated_at,
                created_at=knowledge.created_at,
                metadata=knowledge.metadata, # type: ignore
            )
            for knowledge in knowledges_models
        ]

        return knowledges

    async def update_status_knowledge(self, knowledge_id: UUID, status: KnowledgeStatus):
        knowledge = await self.repository.update_status_knowledge(knowledge_id, status)

        return knowledge
    
    async def get_all_knowledge_in_brain(self, brain_id: UUID) -> List[Knowledge]:
        #FIXME: Implement this method @chloedia
        pass 


    async def get_knowledge(self, knowledge_id: UUID) -> Knowledge:
        inserted_knowledge_db_instance = await self.repository.get_knowledge_by_id(knowledge_id)

        assert inserted_knowledge_db_instance.id, "Knowledge ID not generated"
        inserted_knowledge = Knowledge(
        id= inserted_knowledge_db_instance.id,
        brain_id=inserted_knowledge_db_instance.brain_id,
        file_name=inserted_knowledge_db_instance.file_name,
        url=inserted_knowledge_db_instance.url,
        mime_type=inserted_knowledge_db_instance.mime_type,
        status=inserted_knowledge_db_instance.status,
        source=inserted_knowledge_db_instance.source,
        source_link=inserted_knowledge_db_instance.source_link,
        file_size=inserted_knowledge_db_instance.file_size,
        file_sha1=inserted_knowledge_db_instance.file_sha1,
        updated_at=inserted_knowledge_db_instance.updated_at,
        created_at=inserted_knowledge_db_instance.created_at,
        metadata=inserted_knowledge_db_instance.metadata # type: ignore
        )
        return inserted_knowledge

    async def remove_brain_all_knowledge(self, brain_id: UUID) -> None:
        self.repository.remove_brain_all_knowledge(brain_id)

        logger.info(
            f"All knowledge in brain {brain_id} removed successfully from table"
        )

    async def remove_knowledge(self, knowledge_id: UUID) -> DeleteKnowledgeResponse:
        message = await self.repository.remove_knowledge_by_id(knowledge_id)

        return message