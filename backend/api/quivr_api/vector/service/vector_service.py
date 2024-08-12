from typing import List
from uuid import UUID

from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
from quivr_api.logger import get_logger
from quivr_api.modules.brain.service.brain_service import BrainService
from quivr_api.modules.dependencies import BaseService
from quivr_api.modules.notification.service.notification_service import \
    NotificationService
from quivr_api.modules.prompt.service.prompt_service import PromptService
from quivr_api.vector.entity.vector import Vector
from quivr_api.vector.repository.vectors_repository import VectorRepository

logger = get_logger(__name__)

prompt_service = PromptService()
brain_service = BrainService()
notification_service = NotificationService()


class VectorService(BaseService[VectorRepository]):
    repository_cls = VectorRepository

    def __init__(self, repository: VectorRepository, embeddings: Embeddings):
        self.repository = repository
        self._embedding = embeddings

    async def create_vectors(
        self, chunks: List[Document], knowledge_id: UUID
    ) -> List[str]:
        # Vector is created upon the user's first question asked
        logger.info(
            f"New vector entry in vectors table for knowledge_id {knowledge_id}"
        )
        # FIXME ADD a check in case of failure
        embeddings = self._embedding.embed_documents(
            [chunk.page_content for chunk in chunks]
        )
        new_vectors = [
            Vector(
                content=chunk.page_content,
                metadata_=chunk.metadata,
                embedding=embeddings[i], #type: ignore
                knowledge_id=knowledge_id,
            )
            for i, chunk in enumerate(chunks)
        ]
        created_vector = await self.repository.create_vectors(new_vectors)

        return [str(vector.id) for vector in created_vector]

    async def similarity_search(self, query: str, brain_id: str, k: int = 40) -> List[Document]:
        vectors = self._embedding.embed_documents([query])
        query_embedding = vectors[0]
        vectors = await self.repository.similarity_search(query_embedding, brain_id, k)

        match_result = [
            Document(
                metadata={
                    search.metadata,
                    "id": search.id,
                    "similarity": search.get("similarity", 0.0),
                },
                page_content=search.get("content", ""),
            )
            for search in vectors
            if search.get("content")
        ]

        sorted_match_result_by_file_name_metadata = sorted(
            match_result,
            key=lambda x: (
                x.metadata.get("file_name", ""),
                x.metadata.get("index", float("inf")),
            ),
        )

        return sorted_match_result_by_file_name_metadata
        return vectors
