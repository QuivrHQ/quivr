from typing import Any, List

from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
from langchain_community.vectorstores import SupabaseVectorStore
from logger import get_logger
from supabase.client import Client

logger = get_logger(__name__)


class CustomSupabaseVectorStore(SupabaseVectorStore):
    """A custom vector store that uses the match_vectors table instead of the vectors table."""

    brain_id: str = "none"
    user_id: str = "none"
    number_docs: int = 35
    max_input: int = 2000

    def __init__(
        self,
        client: Client,
        embedding: Embeddings,
        table_name: str,
        brain_id: str = "none",
        user_id: str = "none",
        number_docs: int = 35,
        max_input: int = 2000,
    ):
        super().__init__(client, embedding, table_name)
        self.brain_id = brain_id
        self.user_id = user_id
        self.number_docs = number_docs
        self.max_input = max_input

    def find_brain_closest_query(
        self,
        user_id: str,
        query: str,
        k: int = 6,
        table: str = "match_brain",
        threshold: float = 0.5,
    ) -> [dict]:
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
        full_text_weight: float = 2.0,  # Add this parameter
        semantic_weight: float = 1.0,  # Add this parameter
        rrf_k: int = 1,  # Add this parameter
        k: int = 40,
        table: str = "hybrid_match_vectors",
        threshold: float = 0.5,
        **kwargs: Any,
    ) -> List[Document]:
        vectors = self._embedding.embed_documents([query])
        query_embedding = vectors[0]
        query_lower = query.lower()
        res = self._client.rpc(
            table,
            {
                "query_text": query_lower,
                "match_count": 500,
                "query_embedding": query_embedding,
                "full_text_weight": full_text_weight,  # Add this line
                "semantic_weight": semantic_weight,  # Add this line
                "rrf_k": rrf_k,  # Add this line
                "p_brain_id": str(self.brain_id),
                "max_chunk_sum": self.max_input,
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
        for search in res.data:
            if search.get("content"):
                logger.info("ft_rank: %s", search.get("ft_rank", 0.0))
                logger.info("similarity: %s", search.get("similarity", 0.0))
                logger.info("rank_ix: %s", search.get("rank_ix", 0))

        return match_result
