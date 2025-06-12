from quivr_core.base_config import QuivrBaseConfig
from typing import Optional, Dict, Any


class RetrieverConfig(QuivrBaseConfig):
    k: int = 40  # Number of chunks returned by the retriever
    filter: Optional[Dict[str, Any]] = None
    dynamic_retrieval: bool = False
    dynamic_retrieval_max_iterations: int = 3
    top_n_knowledge: int = 3
