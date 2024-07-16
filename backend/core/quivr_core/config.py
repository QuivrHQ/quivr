from pydantic import BaseModel


class LLMEndpointConfig(BaseModel):
    model: str = "gpt-3.5-turbo-0125"
    llm_base_url: str | None = None
    llm_api_key: str | None = None
    max_input: int = 2000
    max_tokens: int = 2000
    temperature: float = 0.7
    streaming: bool = True


class RAGConfig(BaseModel):
    llm_config: LLMEndpointConfig = LLMEndpointConfig()
    max_history: int = 10
    max_files: int = 20
    prompt: str | None = None
