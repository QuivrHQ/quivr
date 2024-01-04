from typing import Any, List

from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
from langchain.vectorstores import PGVecto_rs


class CustomPGVecto_rsVectorStore(PGVecto_rs):
    """A custom vector store that uses pgvecto.rs for vector similarity searches."""

    brain_id: str = "none"

    def __init__(
        self,
        db_url: str,
        embedding: Embeddings,
        collection_name: str,
        brain_id: str = "none",
    ):
        super().__init__(
            embedding=embedding,
            dimension=len(embedding.embed_query("test")),
            db_url=db_url,
            collection_name=collection_name,
        )
        self.brain_id = brain_id

    def similarity_search(
        self,
        query: str,
        k: int = 6,
        threshold: float = 0.5,
        distance_func: str = "sqrt_euclid",
        **kwargs: Any
    ) -> List[Document]:
        # Perform similarity search using the base class method
        results_with_scores = super().similarity_search_with_score(
            query, k=k, distance_func=distance_func, **kwargs
        )

        # Filter results based on the threshold and extract only the documents
        documents = [doc for doc, score in results_with_scores if score >= threshold]

        return documents
