from typing import Union
from quivr_core.rag.entities.reranker import RerankerConfig, DefaultRerankers
from langchain_cohere import CohereRerank
from langchain_community.document_compressors import JinaRerank
from langchain_core.vectorstores import VectorStore, VectorStoreRetriever
from langchain.retrievers import ContextualCompressionRetriever
from quivr_core.rag.entities.retriever import RetrieverConfig
from langchain_core.documents import Document
from typing import List
import logging

logger = logging.getLogger("quivr_core")


def get_retriever(
    vector_store: VectorStore, retriever_config: RetrieverConfig
) -> VectorStoreRetriever:
    """
    Returns a retriever that can retrieve documents from the vector store.

    Args:
        **kwargs: Additional arguments to pass to the retriever

    Returns:
        VectorStoreRetriever: The retriever instance

    Raises:
        ValueError: If no vector store is provided
    """
    config = {"search_kwargs": retriever_config.model_dump(exclude={"extra_config"})}
    return vector_store.as_retriever(**config)


def get_reranker(reranker_config: RerankerConfig) -> Union[CohereRerank, JinaRerank]:
    """
    Get a reranker instance based on configuration.

    Args:
        **kwargs: Override configuration values

    Returns:
        Document compressor/reranker instance
    """
    config = reranker_config

    reranker: Union[CohereRerank, JinaRerank]

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


def get_compression_retriever(
    vector_store: VectorStore,
    retriever_config: RetrieverConfig,
    reranker_config: RerankerConfig,
) -> ContextualCompressionRetriever:
    """
    Get a compression retriever that combines base retrieval with reranking.

    Args:
        **kwargs: Arguments for retriever and reranker configuration

    Returns:
        ContextualCompressionRetriever instance
    """

    base_retriever = get_retriever(vector_store, retriever_config)
    reranker = get_reranker(reranker_config)

    return ContextualCompressionRetriever(
        base_compressor=reranker, base_retriever=base_retriever
    )


def filter_chunks_by_relevance(
    chunks: List[Document],
    relevance_score_key: str,
    relevance_score_threshold: float | None = None,
):
    if relevance_score_threshold is None:
        return chunks

    filtered_chunks = []
    for chunk in chunks:
        if relevance_score_key not in chunk.metadata:
            logger.warning(
                f"Relevance score key {relevance_score_key} not found in metadata, cannot filter chunks by relevance"
            )
            filtered_chunks.append(chunk)
        elif chunk.metadata[relevance_score_key] >= relevance_score_threshold:
            filtered_chunks.append(chunk)

    return filtered_chunks


def sort_docs_by_relevance(
    docs: List[Document], relevance_score_key: str
) -> List[Document]:
    return sorted(
        docs,
        key=lambda x: x.metadata[relevance_score_key],
        reverse=True,
    )
