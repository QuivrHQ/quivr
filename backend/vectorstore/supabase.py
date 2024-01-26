from typing import Any, List

from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
from langchain.vectorstores import SupabaseVectorStore
from logger import get_logger
from supabase.client import Client

logger = get_logger(__name__)


class CustomSupabaseVectorStore(SupabaseVectorStore):
    """A custom vector store that uses the match_vectors table instead of the vectors table."""

    brain_id: str = "none"
    user_id: str = "none"
    number_docs: int = 35

    def __init__(
        self,
        client: Client,
        embedding: Embeddings,
        table_name: str,
        brain_id: str = "none",
        user_id: str = "none",
        number_docs: int = 35,
    ):
        super().__init__(client, embedding, table_name)
        self.brain_id = brain_id
        self.user_id = user_id
        self.number_docs = number_docs

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
        k: int = 35,
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
                "match_count": self.number_docs,
                "p_brain_id": str(self.brain_id),
            },
        ).execute()

        match_result = [
            (
                Document(
                    metadata={
                        **search.get("metadata", {}),
                        "id": search.get("id", ""),
                        "similarity": search.get("similarity", 0.0),
                    },
                    page_content=search.get("content", ""),
                ),
                search.get("similarity", 0.0),
            )
            for search in res.data
            if search.get("content")
        ]

        documents = [doc for doc, _ in match_result]

        return documents
