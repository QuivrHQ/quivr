from quivr_core.base_config import QuivrBaseConfig
from quivr_core.rag.entities.reranker import RerankerConfig
from quivr_core.rag.entities.retriever import RetrieverConfig


class RetrievalServiceConfig(QuivrBaseConfig):
    reranker_config: RerankerConfig = RerankerConfig()
    retriever_config: RetrieverConfig = RetrieverConfig()
