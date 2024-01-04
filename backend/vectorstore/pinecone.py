from typing import Callable, List, Optional, Union

from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
from langchain.vectorstores import Pinecone
from langchain_community.vectorstores.utils import DistanceStrategy

from pinecone import Index


class CustomPineconeVectorStore(Pinecone):
    """A custom vector store using Pinecone for vector similarity searches."""

    def __init__(
        self,
        index: Index,
        embedding: Union[Embeddings, Callable],
        text_key: str = "text",
        namespace: Optional[str] = None,
        distance_strategy: Optional[DistanceStrategy] = DistanceStrategy.COSINE,
    ):
        """Initialize with Pinecone client."""
        super().__init__(index, embedding, text_key, namespace, distance_strategy)

    def similarity_search(
        self,
        query: str,
        k: int = 6,
        threshold: float = 0.5,
        filter: Optional[dict] = None,
        namespace: Optional[str] = None,
        **kwargs: Any
    ) -> List[Document]:
        """Perform a similarity search with filtering based on a threshold."""
        # Use the namespace set in __init__ if not provided in the method call
        effective_namespace = namespace if namespace is not None else self._namespace

        # Call the base class similarity_search_with_score method
        results_with_scores = super().similarity_search_with_score(
            query, k=k, filter=filter, namespace=effective_namespace, **kwargs
        )

        # Filter results based on the threshold and extract only the documents
        documents = [doc for doc, score in results_with_scores if score >= threshold]

        return documents
