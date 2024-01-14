from typing import Any, List

from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
from langchain.vectorstores import SupabaseVectorStore
from supabase.client import Client


class CustomSupabaseVectorStore(SupabaseVectorStore):
    """A custom vector store that uses the match_vectors table instead of the vectors table."""

    brain_id: str = "none"
    number_docs: int = 4

    def __init__(
        self,
        client: Client,
        embedding: Embeddings,
        table_name: str,
        brain_id: str = "none",
        number_docs: int = 4,
    ):
        super().__init__(client, embedding, table_name)
        self.brain_id = brain_id
        self.number_docs = number_docs

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        table: str = "match_vectors",
        threshold: float = 0.5,
        **kwargs: Any
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
