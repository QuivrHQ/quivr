from typing import Any, Callable, List, Optional

from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
from langchain.vectorstores import Weaviate

from weaviate import Client


class CustomWeaviateVectorStore(Weaviate):
    """A custom vector store using Weaviate for vector similarity searches."""

    brain_id: str = "none"

    def __init__(
        self,
        client: Client,
        embedding: Embeddings,
        index_name: str,
        text_key: str = "text",
        attributes: Optional[List[str]] = None,
        relevance_score_fn: Optional[Callable[[float], float]] = None,
        by_text: bool = True,
        brain_id: str = "none",
    ):
        super().__init__(
            client,
            index_name,
            text_key,
            embedding,
            attributes,
            relevance_score_fn,
            by_text,
        )
        self.brain_id = brain_id

    def similarity_search(
        self, query: str, k: int = 6, threshold: float = 0.5, **kwargs: Any
    ) -> List[Document]:
        # Perform similarity search using the base class method
        results_with_scores = super().similarity_search_with_score(query, k=k, **kwargs)

        # Filter results based on the threshold and extract only the documents
        documents = [
            doc for doc, score in results_with_scores if 1 - score >= threshold
        ]

        return documents
