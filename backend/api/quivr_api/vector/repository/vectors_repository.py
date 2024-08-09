from typing import Any, List

from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
from pgvector.sqlalchemy import Vector as PGVector
from sqlalchemy import exc, text
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_api.modules.dependencies import BaseRepository
from quivr_api.vector.entity.vector import Vector


class VectorRepository(BaseRepository):
    def __init__(self, session: AsyncSession, embeddings: Embeddings):
        super().__init__(session)
        self.session = session
        self._embedding = embeddings

    async def create_vectors(self, new_vectors: List[Vector]) -> List[Vector]:
        if len(new_vectors) > 0:
            # Embed the vector content if it doesn't already have an embedding
            embeddings = self._embedding.embed_documents(
                [new_vector.content for new_vector in new_vectors]
            )
            for new_vector, embedding in zip(new_vectors, embeddings):
                new_vector.embedding = PGVector(embedding)

        try:
            # Use SQLAlchemy session to add and commit the new vector
            self.session.add_all(new_vectors)
            await self.session.commit()
        except exc.IntegrityError:
            # Rollback the session if there’s an IntegrityError
            await self.session.rollback()
            raise Exception("Integrity error occurred while creating vector.")
        # Refresh the session to get any updated fields (like auto-generated IDs)
        await self.session.refresh(new_vectors)

        return new_vectors

    async def similarity_search(
        self,
        query: str,
        brain_id: str,
        k: int = 40,
        max_chunk_sum: int = 10000,  # Example value
        **kwargs: Any,
    ) -> List[Document]:
        vectors = self._embedding.embed_documents([query])
        query_embedding = vectors[0]

        sql_query = text("""
            WITH ranked_vectors AS (
                SELECT
                    v.id AS vector_id,
                    kb.brain_id AS vector_brain_id,
                    v.content AS vector_content,
                    v.metadata AS vector_metadata,
                    v.embedding AS vector_embedding,
                    1 - (v.embedding <=> :query_embedding) AS calculated_similarity,
                    (v.metadata->>'chunk_size')::integer AS chunk_size
                FROM
                    vectors v
                INNER JOIN
                    knowledge_brain kb ON v.knowledge_id = kb.knowledge_id
                WHERE
                    kb.brain_id = :p_brain_id
                ORDER BY
                    calculated_similarity DESC
            ), filtered_vectors AS (
                SELECT
                    vector_id,
                    vector_brain_id,
                    vector_content,
                    vector_metadata,
                    vector_embedding,
                    calculated_similarity,
                    chunk_size,
                    sum(chunk_size) OVER (ORDER BY calculated_similarity DESC) AS running_total
                FROM ranked_vectors
            )
            SELECT
                vector_id AS id,
                vector_brain_id AS brain_id,
                vector_content AS content,
                vector_metadata AS metadata,
                vector_embedding AS embedding,
                calculated_similarity AS similarity
            FROM filtered_vectors
            WHERE running_total <= :max_chunk_sum
            LIMIT :k
        """)

        params = {
            "query_embedding": query_embedding,
            "p_brain_id": brain_id,
            "k": k,
            "max_chunk_sum": max_chunk_sum,
        }

        result = await self.session.execute(sql_query, params=params)

        # return all in document format
        return [Document(**dict(row)) for row in result.all()]
