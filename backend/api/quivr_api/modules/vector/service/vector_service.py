from typing import List
from uuid import UUID

from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
from quivr_api.logger import get_logger
from quivr_api.modules.dependencies import BaseService, get_embedding_client
from quivr_api.modules.vector.entity.vector import Vector
from quivr_api.modules.vector.repository.vectors_repository import VectorRepository

logger = get_logger(__name__)


class VectorService(BaseService[VectorRepository]):
    repository_cls = VectorRepository

    def __init__(
        self, repository: VectorRepository, embedder: Embeddings | None = None
    ):
        if embedder is None:
            self.embedder = get_embedding_client()
        else:
            self.embedder = embedder

        self.repository = repository

    async def create_vectors(
        self, chunks: List[Document], knowledge_id: UUID, autocommit: bool = True
    ) -> List[UUID]:
        # Vector is created upon the user's first question asked
        logger.info(
            f"New vector entry in vectors table for knowledge_id {knowledge_id}"
        )
        # FIXME ADD a check in case of failure
        embeddings = self.embedder.embed_documents(
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
        created_vector = await self.repository.create_vectors(new_vectors, autocommit)

        return [vector.id for vector in created_vector if vector.id]

    async def similarity_search(self, query: str, brain_id: UUID, k: int = 40):
        vectors = self.embedder.embed_documents([query])
        query_embedding = vectors[0]
        vectors = await self.repository.similarity_search(
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
