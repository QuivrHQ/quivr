from quivr_core.base_config import QuivrBaseConfig
from typing import Optional, Dict, Any


class RetrieverExtraConfig(QuivrBaseConfig):
    top_n_knowledge: int = 3
    dynamic_retrieval_max_iterations: int = 3


class RetrieverConfig(QuivrBaseConfig):
    k: int = 40  # Number of chunks returned by the retriever
    filter: Optional[Dict[str, Any]] = None
    max_chunk_sum: int = 10000
    extra_config: RetrieverExtraConfig = RetrieverExtraConfig()
