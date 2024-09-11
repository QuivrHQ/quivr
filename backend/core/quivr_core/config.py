from quivr_core.processor.splitter import SplitterConfig
from quivr_core.processor.implementations.megaparse_config import MegaparseConfig
from quivr_core.base_config import QuivrBaseConfig

RERANKERS_DEFAULT_MODELS = {
    'cohere': "rerank-multilingual-v3.0",
    'jina': "jina-reranker-v2-base-multilingual",
    # Add more suppliers as needed
}

class LLMEndpointConfig(QuivrBaseConfig):
    model: str = "gpt-3.5-turbo-0125"
    llm_base_url: str | None = None
    llm_api_key: str | None = None
    max_input: int = 2000
    max_tokens: int = 2000
    temperature: float = 0.7
    streaming: bool = True

# Cannot use Pydantic v2 field_validator because of conflicts with pydantic v1 still in use in LangChain
class RerankerConfig(QuivrBaseConfig):
    supplier: str | None = None
    model: str | None = None
    top_n: int = 5

    def __init__(self, **data):
        super().__init__(**data)  # Call Pydantic's BaseModel init
        self.validate_model()  # Automatically call external validation

    def validate_model(self):
        # Custom external validation logic
        if self.model is None and self.supplier is not None:
            # Set default model based on supplier if not provided
            try:
                self.model = RERANKERS_DEFAULT_MODELS[self.supplier]
            except:
                raise ValueError(f"Unknown supplier: {self.supplier}")

class RetrievalConfig(QuivrBaseConfig):
    reranker_config: RerankerConfig = RerankerConfig()

class ParserConfig(QuivrBaseConfig):
    splitter_config: SplitterConfig = SplitterConfig()
    megaparse_config: MegaparseConfig = MegaparseConfig()

class IngestionConfig(QuivrBaseConfig):
    parser_config: ParserConfig = ParserConfig()

class RAGConfig(QuivrBaseConfig):
    retrieval_config: RetrievalConfig = RetrievalConfig()
    ingestion_config: IngestionConfig = IngestionConfig()
    llm_config: LLMEndpointConfig = LLMEndpointConfig()
    max_history: int = 10
    max_files: int = 20
    prompt: str | None = None


