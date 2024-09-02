from typing import List
from uuid import UUID

from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
from quivr_api.logger import get_logger
from quivr_api.modules.dependencies import BaseService, get_embedding_client
from quivr_api.vector.entity.vector import Vector
from quivr_api.vector.repository.vectors_repository import VectorRepository

logger = get_logger(__name__)


class VectorService(BaseService[VectorRepository]):
    repository_cls = VectorRepository
    _embedding: Embeddings = get_embedding_client()

    def __init__(self, repository: VectorRepository):
        self.repository = repository

    def create_vectors(self, chunks: List[Document], knowledge_id: UUID) -> List[UUID]:
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
                embedding=embeddings[i],  # type: ignore
                knowledge_id=knowledge_id,
            )
            for i, chunk in enumerate(chunks)
        ]
        created_vector = self.repository.create_vectors(new_vectors)

        return [vector.id for vector in created_vector if vector.id]

    def similarity_search(self, query: str, brain_id: UUID, k: int = 40):
        vectors = self._embedding.embed_documents([query])
        query_embedding = vectors[0]
        vectors = self.repository.similarity_search(
            query_embedding=query_embedding, brain_id=brain_id, k=k
        )

        match_result = [
            Document(
                metadata={
                    **search.metadata_,
                    "id": search.id,
                    "similarity": search.similarity,
                },
                page_content=search.content,
            )
            for search in vectors
            if search.content
        ]

        return match_result
