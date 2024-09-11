from quivr_core.base_config import QuivrBaseConfig


class MegaparseConfig(QuivrBaseConfig):
    strategy: str = "fast"
    llama_parse_api_key: str | None = None