from typing import List
from uuid import UUID

from langchain.docstore.document import Document

from quivr_api.logger import get_logger
from quivr_api.modules.brain.service.brain_service import BrainService
from quivr_api.modules.dependencies import BaseService
from quivr_api.modules.notification.service.notification_service import (
    NotificationService,
)
from quivr_api.modules.prompt.service.prompt_service import PromptService
from quivr_api.vector.entity.vector import Vector
from quivr_api.vector.repository.vectors_repository import VectorRepository

logger = get_logger(__name__)

prompt_service = PromptService()
brain_service = BrainService()
notification_service = NotificationService()


class VectorService(BaseService[VectorRepository]):
    repository_cls = VectorRepository

    def __init__(self, repository: VectorRepository):
        self.repository = repository

    async def create_vectors(
        self, chunks: List[Document], knowledge_id: UUID
    ) -> List[str]:
        # Vector is created upon the user's first question asked
        logger.info(
            f"New vector entry in vectors table for knowledge_id {knowledge_id}"
        )
        # FIXME ADD a check in case of failure
        new_vectors = [
            Vector(
                content=chunk.page_content,
                metadata_=chunk.metadata,
                embedding=None,
                knowledge_id=knowledge_id,
            )
            for chunk in chunks
        ]
        created_vector = await self.repository.create_vectors(new_vectors)

        return [str(vector.id) for vector in created_vector]
