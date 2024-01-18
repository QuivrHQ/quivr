from typing import Any, Dict, List, Optional

from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
from langchain.vectorstores import SupabaseVectorStore

from supabase.client import Client


class CustomSupabaseVectorStore(SupabaseVectorStore):
    """A custom vector store using Supabase for vector similarity searches."""

    brain_id: str = "none"

    def __init__(
        self,
        client: Client,
        embedding: Embeddings,
        table_name: str = "match_vectors",
        brain_id: str = "none",
    ):
        super().__init__(client, embedding, table_name)
        self.brain_id = brain_id

    def similarity_search(
        self,
        query: str,
        k: int = 6,
        threshold: float = 0.5,
        filter: Optional[Dict[str, Any]] = None,
        postgrest_filter: Optional[str] = None,
        **kwargs: Any
    ) -> List[Document]:
        # Perform the similarity search using the base class method
        # score_threshold is passed as a part of kwargs
        results_with_scores = super().similarity_search(
            query,
            k=k,
            filter=filter,
            postgrest_filter=postgrest_filter,
            score_threshold=threshold,
            **kwargs
        )

        # Extract only the documents, assuming results are tuples of (Document, similarity_score)
        documents = [doc for doc, score in results_with_scores]

        return documents
