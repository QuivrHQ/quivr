from typing import Any, List
from uuid import UUID

from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
from langchain_community.vectorstores import SupabaseVectorStore

from quivr_api.logger import get_logger

# from quivr_api.modules.dependencies import get_pg_database_engine
from quivr_api.modules.vector.service.vector_service import VectorService
from supabase.client import Client

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
        vector_service: VectorService,
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
        self.vector_service = vector_service

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
        logger.debug(f"Similarity search for query: {query}")
        assert self.brain_id, "Brain ID is required for similarity search"

        match_result = self.vector_service.similarity_search(
            query, brain_id=self.brain_id, k=k
        )

        sorted_match_result_by_file_name_metadata = sorted(
            match_result,
            key=lambda x: (
                x.metadata.get("file_name", ""),
                x.metadata.get("index", float("inf")),
            ),
        )

        return sorted_match_result_by_file_name_metadata
