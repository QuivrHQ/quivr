from typing import Any, List
from uuid import UUID

from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
from langchain_community.vectorstores import SupabaseVectorStore

# from quivr_api.modules.dependencies import get_pg_database_engine
from supabase.client import Client

from quivr_api.logger import get_logger

logger = get_logger(__name__)
# engine = get_pg_database_engine()
# Session = sessionmaker(bind=engine)


class CustomSupabaseVectorStore(SupabaseVectorStore):
    """A custom vector store that uses the match_vectors table instead of the vectors table."""

    def __init__(
        self,
        client: Client,
        embedding: Embeddings,
        table_name: str,
        brain_id: UUID | None = None,
        user_id: UUID | None = None,
        number_docs: int = 35,
        max_input: int = 2000,
    ):
        super().__init__(client, embedding, table_name)
        self.brain_id = brain_id
        self.user_id = user_id
        self.number_docs = number_docs
        self.max_input = max_input

    def add_knowledge_id_to_vector(self, knowledge_id: UUID, vector_id: UUID) -> Any:
        return (
            self._client.table("vectors")
            .update({"knowledge_id": knowledge_id})
            .eq("id", vector_id)
            .execute()
        )

    def find_brain_closest_query(
        self,
        user_id: str,
        query: str,
        k: int = 6,
        table: str = "match_brain",
        threshold: float = 0.5,
    ) -> list[dict[str, Any]]:
        vectors = self._embedding.embed_documents([query])
        query_embedding = vectors[0]

        res = self._client.rpc(
            table,
            {
                "query_embedding": query_embedding,
                "match_count": self.number_docs,
                "p_user_id": str(self.user_id),
            },
        ).execute()

        # Get the brain_id of the brain that is most similar to the query
        # Get the brain_id and name of the brains that are most similar to the query
        brain_details = [
            {
                "id": item.get("id", None),
                "name": item.get("name", None),
                "similarity": item.get("similarity", 0.0),
            }
            for item in res.data
        ]
        return brain_details

    def similarity_search(
        self,
        query: str,
        k: int = 40,
        table: str = "match_vectors",
        threshold: float = 0.5,
        **kwargs: Any,
    ) -> List[Document]:
        vectors = self._embedding.embed_documents([query])
        query_embedding = vectors[0]
        res = self._client.rpc(
            table,
            {
                "query_embedding": query_embedding,
                "max_chunk_sum": self.max_input,
                "p_brain_id": str(self.brain_id),
            },
        ).execute()

        match_result = [
            Document(
                metadata={
                    **search.get("metadata", {}),
                    "id": search.get("id", ""),
                    "similarity": search.get("similarity", 0.0),
                },
                page_content=search.get("content", ""),
            )
            for search in res.data
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

    # def similarity_search(
    #     self,
    #     query: str,
    #     k: int = 40,
    #     threshold: float = 0.5,
    #     **kwargs: Any,
    # ) -> List[Document]:

    #     # Generate embedding for the query
    #     vectors = self._embedding.embed_documents([query])
    #     query_embedding = vectors[0]

    #     # SQL query to search for similar documents
    #     sql_query = '''
    #     WITH ranked_vectors AS (
    #         SELECT
    #             v.id AS vector_id,
    #             kb.brain_id AS vector_brain_id,
    #             v.content AS vector_content,
    #             v.metadata AS vector_metadata,
    #             v.embedding AS vector_embedding,
    #             1 - (v.embedding <=> :query_embedding) AS calculated_similarity,
    #             (v.metadata->>'chunk_size')::integer AS chunk_size
    #         FROM
    #             vectors v
    #         INNER JOIN
    #             knowledge_brain kb ON v.knowledge_id = kb.knowledge_id
    #         WHERE
    #             kb.brain_id = :p_brain_id
    #         ORDER BY
    #             calculated_similarity DESC
    #     ), filtered_vectors AS (
    #         SELECT
    #             vector_id,
    #             vector_brain_id,
    #             vector_content,
    #             vector_metadata,
    #             vector_embedding,
    #             calculated_similarity,
    #             chunk_size,
    #             sum(chunk_size) OVER (ORDER BY calculated_similarity DESC) AS running_total
    #         FROM ranked_vectors
    #     )
    #     SELECT
    #         vector_id AS id,
    #         vector_brain_id AS brain_id,
    #         vector_content AS content,
    #         vector_metadata AS metadata,
    #         vector_embedding AS embedding,
    #         calculated_similarity AS similarity
    #     FROM filtered_vectors
    #     WHERE running_total <= :max_chunk_sum
    #     LIMIT :k
    #     '''

    #     try:
    #         # Execute the SQL query with parameters
    #         res = self.session.execute(text(sql_query), {
    #                 "query_embedding": query_embedding,
    #                 "max_chunk_sum": self.max_input,
    #                 "p_brain_id": str(self.brain_id),
    #                 "k": k
    #             })

    #         logger.debug(f"Similarity search results: {res}")

    #         # Process and structure the results into Document objects
    #         match_result = [
    #             Document(
    #                 metadata={
    #                     **search.get("metadata", {}),
    #                     "id": search.get("id", ""),
    #                     "similarity": search.get("similarity", 0.0),
    #                 },
    #                 page_content=search.get("content", ""),
    #             )
    #             for search in res.data
    #             if search.get("content")
    #         ]

    #         # Sort results by file name and index for consistency
    #         sorted_match_result_by_file_name_metadata = sorted(
    #             match_result,
    #             key=lambda x: (
    #                 x.metadata.get("file_name", ""),
    #                 x.metadata.get("index", float("inf")),
    #             ),
    #         )

    #         return sorted_match_result_by_file_name_metadata

    #     except Exception as e:
    #         # Handle any errors that occur during the process
    #         print(f"An error occurred during similarity search: {e}")
    #         return []
