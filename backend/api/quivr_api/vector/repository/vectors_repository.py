from typing import Any, List, Sequence
from uuid import UUID

from quivr_api.logger import get_logger
from quivr_api.modules.dependencies import BaseRepository
from quivr_api.vector.entity.vector import SimilaritySearchOutput, Vector
from sqlalchemy import exc, text
from sqlmodel import Session, select

logger = get_logger(__name__)


class VectorRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)
        self.session = session

    def create_vectors(self, new_vectors: List[Vector]) -> List[Vector]:
        try:
            # Use SQLAlchemy session to add and commit the new vector
            self.session.add_all(new_vectors)
            self.session.commit()
        except exc.IntegrityError:
            # Rollback the session if there’s an IntegrityError
            self.session.rollback()
            raise Exception("Integrity error occurred while creating vector.")
        except Exception as e:
            self.session.rollback()
            print(f"Error: {e}")
            raise Exception(f"An error occurred while creating vector: {e}")

        # Refresh the session to get any updated fields (like auto-generated IDs)
        for vector in new_vectors:
            self.session.refresh(vector)

        return new_vectors

    def get_vectors_by_knowledge_id(self, knowledge_id: UUID) -> Sequence[Vector]:
        query = select(Vector).where(Vector.knowledge_id == knowledge_id)
        results = self.session.execute(query)
        return results.scalars().all()

    def similarity_search(
        self,
        query_embedding: List[float],
        brain_id: UUID,
        k: int = 40,
        max_chunk_sum: int = 10000,  # Example value
        **kwargs: Any,
    ) -> Sequence[SimilaritySearchOutput]:
        sql_query = text("""
            WITH ranked_vectors AS (
            SELECT
                v.id AS vector_id,
                kb.brain_id AS vector_brain_id,
                v.knowledge_id AS vector_knowledge_id,
                v.content AS vector_content,
                v.metadata AS vector_metadata,
                v.embedding AS vector_embedding,
                1 - (v.embedding <=> (:query_embedding)::vector) AS calculated_similarity,
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
                vector_knowledge_id,
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
            vector_knowledge_id AS knowledge_id,
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

        result = self.session.execute(sql_query, params=params)
        full_results = result.all()
        formated_result = [
            SimilaritySearchOutput(
                id=row.id,
                brain_id=row.brain_id,
                knowledge_id=row.knowledge_id,
                content=row.content,
                metadata_=row.metadata,
                embedding=row.embedding,
                similarity=row.similarity,
            )
            for row in full_results
        ]
        return formated_result
