import logging
from typing import List
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from langchain.retrievers import ContextualCompressionRetriever
from langchain_community.document_compressors import JinaRerank
from langchain_cohere import CohereRerank


from quivr_core.rag.entities.reranker import RerankerConfig, DefaultRerankers
from quivr_core.rag.entities.retriever import RetrieverConfig

logger = logging.getLogger("quivr_core")


class RetrievalService:
    """Service for document retrieval, reranking, and filtering operations."""

    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    def get_retriever(self, retriever_config: RetrieverConfig):
        """
        Returns a retriever that can retrieve documents from the vector store.

        Args:
            **kwargs: Additional arguments to pass to the retriever

        Returns:
            VectorStoreRetriever: The retriever instance

        Raises:
            ValueError: If no vector store is provided
        """
        config = {"search_kwargs": retriever_config}

        if self.vector_store:
            return self.vector_store.as_retriever(**config)
        else:
            raise ValueError("No vector store provided")

    def get_reranker(self, reranker_config: RerankerConfig):
        """
        Get a reranker instance based on configuration.

        Args:
            **kwargs: Override configuration values

        Returns:
            Document compressor/reranker instance
        """
        config = reranker_config

        if config.supplier == DefaultRerankers.COHERE:
            reranker = CohereRerank(
                model=config.model, top_n=config.top_n, cohere_api_key=config.api_key
            )
        elif config.supplier == DefaultRerankers.JINA:
            reranker = JinaRerank(
                model=config.model, top_n=config.top_n, jina_api_key=config.api_key
            )
        else:
            raise ValueError(f"Invalid reranker supplier: {config.supplier}")

        return reranker

    def filter_chunks_by_relevance(
        self,
        chunks: List[Document],
        relevance_score_threshold: float | None = None,
        relevance_score_key: str | None = None,
    ) -> List[Document]:
        """
        Filter documents based on relevance score threshold.

        Args:
            chunks: List of documents to filter
            **kwargs: Additional arguments including relevance_score_threshold

        Returns:
            List of filtered documents
        """

        if relevance_score_threshold is None:
            return chunks

        filtered_chunks = []
        for chunk in chunks:
            if relevance_score_key not in chunk.metadata:
                logger.error(
                    f"Relevance score key {relevance_score_key} not found in metadata, "
                    "cannot filter chunks by relevance"
                )
                raise ValueError(
                    f"Relevance score key {relevance_score_key} not found in metadata, "
                    "cannot filter chunks by relevance"
                )
            elif chunk.metadata[relevance_score_key] >= relevance_score_threshold:
                filtered_chunks.append(chunk)

        return filtered_chunks

    def get_compression_retriever(
        self, retriever_config: RetrieverConfig, reranker_config: RerankerConfig
    ) -> ContextualCompressionRetriever:
        """
        Get a compression retriever that combines base retrieval with reranking.

        Args:
            **kwargs: Arguments for retriever and reranker configuration

        Returns:
            ContextualCompressionRetriever instance
        """

        base_retriever = self.get_retriever(retriever_config)
        reranker = self.get_reranker(reranker_config)

        return ContextualCompressionRetriever(
            base_compressor=reranker, base_retriever=base_retriever
        )

    async def retrieve_documents(
        self,
        query: str,
        reranker_config: RerankerConfig,
        retriever_config: RetrieverConfig,
    ) -> List[Document]:
        """
        Retrieve and rerank documents for a given query.

        Args:
            query: The search query
            filter_dict: Optional filter to apply to search
            **kwargs: Additional arguments for retrieval configuration

        Returns:
            List of retrieved and filtered documents
        """

        # Get compression retriever
        compression_retriever = self.get_compression_retriever(
            retriever_config=retriever_config, reranker_config=reranker_config
        )

        # Retrieve documents
        docs = await compression_retriever.ainvoke(query)

        # Apply relevance filtering
        filtered_docs = self.filter_chunks_by_relevance(
            docs,
            relevance_score_threshold=reranker_config.relevance_score_threshold,
            relevance_score_key=reranker_config.relevance_score_key,
        )

        return filtered_docs

    async def retrieve_documents_dynamic(
        self,
        query: str,
        reranker_config: RerankerConfig,
        retriever_config: RetrieverConfig,
    ) -> List[Document]:
        """
        Dynamically retrieve documents, increasing search parameters if needed.

        Args:
            query: The search query
            filter_dict: Optional filter to apply to search
            max_iterations: Maximum number of retrieval attempts
            **kwargs: Additional arguments for retrieval configuration

        Returns:
            List of retrieved and filtered documents
        """
        top_n = reranker_config.top_n
        k = retriever_config.k

        number_of_relevant_chunks = top_n
        iteration = 1

        while (
            number_of_relevant_chunks == top_n
            and iteration <= retriever_config.dynamic_retrieval_max_iterations
        ):
            current_top_n = top_n * iteration
            current_k = max([current_top_n * 2, k])

            if iteration > 1:
                logger.info(
                    f"Increasing top_n to {current_top_n} and k to {current_k} "
                    "to retrieve more relevant chunks"
                )

            compression_retriever = self.get_compression_retriever(
                retriever_config=retriever_config, reranker_config=reranker_config
            )

            docs = await compression_retriever.ainvoke(query)
            filtered_docs = self.filter_chunks_by_relevance(
                docs,
                relevance_score_threshold=reranker_config.relevance_score_threshold,
                relevance_score_key=reranker_config.relevance_score_key,
            )

            number_of_relevant_chunks = len(filtered_docs)
            iteration += 1

            # If we got fewer docs than requested, no need to continue
            if number_of_relevant_chunks < current_top_n:
                break

        return filtered_docs

    def sort_docs_by_relevance(
        self, docs: List[Document], relevance_score_key: str
    ) -> List[Document]:
        """
        Sort documents by relevance score in descending order.

        Args:
            docs: List of documents to sort

        Returns:
            List of documents sorted by relevance
        """

        def get_relevance_score(doc: Document) -> float:
            return doc.metadata.get(relevance_score_key, 0.0)

        return sorted(docs, key=get_relevance_score, reverse=True)
