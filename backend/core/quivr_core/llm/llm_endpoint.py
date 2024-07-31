from langchain_core.language_models.chat_models import BaseChatModel
from pydantic.v1 import SecretStr
from quivr_core.brain.info import LLMInfo
from quivr_core.config import LLMEndpointConfig
from quivr_core.utils import model_supports_function_calling


class LLMEndpoint:
    def __init__(self, llm_config: LLMEndpointConfig, llm: BaseChatModel):
        self._config = llm_config
        self._llm = llm
        self._supports_func_calling = model_supports_function_calling(
            self._config.model
        )

    def get_config(self):
        return self._config

    @classmethod
    def from_config(cls, config: LLMEndpointConfig = LLMEndpointConfig()):
        try:
            from langchain_openai import ChatOpenAI

            _llm = ChatOpenAI(
                model=config.model,
                api_key=SecretStr(config.llm_api_key) if config.llm_api_key else None,
                base_url=config.llm_base_url,
            )
            return cls(llm=_llm, llm_config=config)

        except ImportError as e:
            raise ImportError(
                "Please provide a valid BaseLLM or install quivr-core['base'] package"
            ) from e

    def supports_func_calling(self) -> bool:
        return self._supports_func_calling

    def info(self) -> LLMInfo:
        return LLMInfo(
            model=self._config.model,
            llm_base_url=(
                self._config.llm_base_url if self._config.llm_base_url else "openai"
            ),
            temperature=self._config.temperature,
            max_tokens=self._config.max_tokens,
            supports_function_calling=self.supports_func_calling(),
        )
