import logging
import os
from enum import Enum
from typing import Any, Dict, Hashable, List, Optional, Type, Union, TypeVar
from uuid import UUID

from langchain_core.prompts.base import BasePromptTemplate
from langgraph.graph import END, START
from pydantic import BaseModel, field_serializer
from quivr_core.llm_tools.registry import tool_registry
from quivr_core.rag.entities.prompt import PromptConfig

from quivr_core.base_config import QuivrBaseConfig
from quivr_core.config import MegaparseConfig
from quivr_core.processor.splitter import SplitterConfig
from quivr_core.rag.entities.retriever import RetrieverConfig
from quivr_core.rag.entities.reranker import RerankerConfig
from quivr_core.rag.entities.utils import normalize_to_env_variable_name
from quivr_core.rag.langgraph_framework.entities.filter_history_config import (
    FilterHistoryConfig,
)


logger = logging.getLogger("quivr_core")

T = TypeVar("T", bound=QuivrBaseConfig)

MIN_CONTEXT_TOKENS = 4096
MIN_OUTPUT_TOKENS = 4096


class SpecialEdges(str, Enum):
    start = "START"
    end = "END"


class BrainConfig(QuivrBaseConfig):
    brain_id: UUID | None = None
    name: str

    @property
    def id(self) -> UUID | None:
        return self.brain_id


class DefaultWebSearchTool(str, Enum):
    TAVILY = "tavily"


class DefaultModelSuppliers(str, Enum):
    OPENAI = "openai"
    AZURE = "azure"
    ANTHROPIC = "anthropic"
    META = "meta"
    MISTRAL = "mistral"
    GROQ = "groq"
    GEMINI = "gemini"


class LLMConfig(QuivrBaseConfig):
    max_context_tokens: int | None = None
    max_output_tokens: int | None = None
    tokenizer_hub: str | None = None


class LLMModelConfig:
    _model_defaults: Dict[DefaultModelSuppliers, Dict[str, LLMConfig]] = {
        DefaultModelSuppliers.OPENAI: {
            "gpt-4.1": LLMConfig(
                max_context_tokens=1047576,
                max_output_tokens=32768,
                tokenizer_hub="Quivr/gpt-4o",
            ),
            "gpt-4o": LLMConfig(
                max_context_tokens=128000,
                max_output_tokens=16384,
                tokenizer_hub="Quivr/gpt-4o",
            ),
            "gpt-4o-mini": LLMConfig(
                max_context_tokens=128000,
                max_output_tokens=16384,
                tokenizer_hub="Quivr/gpt-4o",
            ),
            "o3-mini": LLMConfig(
                max_context_tokens=200000,
                max_output_tokens=100000,
                tokenizer_hub="Quivr/gpt-4o",
            ),
            "o4-mini": LLMConfig(
                max_context_tokens=200000,
                max_output_tokens=100000,
                tokenizer_hub="Quivr/gpt-4o",
            ),
            "o1-mini": LLMConfig(
                max_context_tokens=128000,
                max_output_tokens=65536,
                tokenizer_hub="Quivr/gpt-4o",
            ),
            "o1-preview": LLMConfig(
                max_context_tokens=128000,
                max_output_tokens=32768,
                tokenizer_hub="Quivr/gpt-4o",
            ),
            "o1": LLMConfig(
                max_context_tokens=200000,
                max_output_tokens=100000,
                tokenizer_hub="Quivr/gpt-4o",
            ),
            "gpt-4-turbo": LLMConfig(
                max_context_tokens=128000,
                max_output_tokens=4096,
                tokenizer_hub="Quivr/gpt-4",
            ),
            "gpt-4": LLMConfig(
                max_context_tokens=8192,
                max_output_tokens=8192,
                tokenizer_hub="Quivr/gpt-4",
            ),
            "gpt-3.5-turbo": LLMConfig(
                max_context_tokens=16385,
                max_output_tokens=4096,
                tokenizer_hub="Quivr/gpt-3.5-turbo",
            ),
            "text-embedding-3-large": LLMConfig(
                max_context_tokens=8191, tokenizer_hub="Quivr/text-embedding-ada-002"
            ),
            "text-embedding-3-small": LLMConfig(
                max_context_tokens=8191, tokenizer_hub="Quivr/text-embedding-ada-002"
            ),
            "text-embedding-ada-002": LLMConfig(
                max_context_tokens=8191, tokenizer_hub="Quivr/text-embedding-ada-002"
            ),
        },
        DefaultModelSuppliers.ANTHROPIC: {
            "claude-opus-4": LLMConfig(
                max_context_tokens=200000,
                max_output_tokens=8192,
                tokenizer_hub="Quivr/claude-tokenizer",
            ),
            "claude-sonnet-4": LLMConfig(
                max_context_tokens=200000,
                max_output_tokens=8192,
                tokenizer_hub="Quivr/claude-tokenizer",
            ),
            "claude-3-7-sonnet": LLMConfig(
                max_context_tokens=200000,
                max_output_tokens=8192,
                tokenizer_hub="Quivr/claude-tokenizer",
            ),
            "claude-3-5-sonnet": LLMConfig(
                max_context_tokens=200000,
                max_output_tokens=8192,
                tokenizer_hub="Quivr/claude-tokenizer",
            ),
            "claude-3-opus": LLMConfig(
                max_context_tokens=200000,
                max_output_tokens=4096,
                tokenizer_hub="Quivr/claude-tokenizer",
            ),
            "claude-3-sonnet": LLMConfig(
                max_context_tokens=200000,
                max_output_tokens=4096,
                tokenizer_hub="Quivr/claude-tokenizer",
            ),
            "claude-3-haiku": LLMConfig(
                max_context_tokens=200000,
                max_output_tokens=4096,
                tokenizer_hub="Quivr/claude-tokenizer",
            ),
            "claude-2-1": LLMConfig(
                max_context_tokens=200000,
                max_output_tokens=4096,
                tokenizer_hub="Quivr/claude-tokenizer",
            ),
            "claude-2-0": LLMConfig(
                max_context_tokens=100000,
                max_output_tokens=4096,
                tokenizer_hub="Quivr/claude-tokenizer",
            ),
            "claude-instant-1-2": LLMConfig(
                max_context_tokens=100000,
                max_output_tokens=4096,
                tokenizer_hub="Quivr/claude-tokenizer",
            ),
        },
        # Unclear for LLAMA models...
        # see https://huggingface.co/meta-llama/Llama-3.1-405B-Instruct/discussions/6
        DefaultModelSuppliers.META: {
            "llama-3.1": LLMConfig(
                max_context_tokens=128000,
                max_output_tokens=4096,
                tokenizer_hub="Quivr/Meta-Llama-3.1-Tokenizer",
            ),
            "llama-3": LLMConfig(
                max_context_tokens=8192,
                max_output_tokens=2048,
                tokenizer_hub="Quivr/llama3-tokenizer-new",
            ),
            "code-llama": LLMConfig(
                max_context_tokens=16384, tokenizer_hub="Quivr/llama-code-tokenizer"
            ),
        },
        DefaultModelSuppliers.GROQ: {
            "llama-3.3-70b": LLMConfig(
                max_context_tokens=128000,
                max_output_tokens=32768,
                tokenizer_hub="Quivr/Meta-Llama-3.1-Tokenizer",
            ),
            "llama-3.1-70b": LLMConfig(
                max_context_tokens=128000,
                max_output_tokens=32768,
                tokenizer_hub="Quivr/Meta-Llama-3.1-Tokenizer",
            ),
            "llama-3": LLMConfig(
                max_context_tokens=8192, tokenizer_hub="Quivr/llama3-tokenizer-new"
            ),
            "code-llama": LLMConfig(
                max_context_tokens=16384, tokenizer_hub="Quivr/llama-code-tokenizer"
            ),
            "deepseek-r1-distill-llama-70b": LLMConfig(
                max_context_tokens=128000,
                max_output_tokens=32768,
                tokenizer_hub="Quivr/Meta-Llama-3.1-Tokenizer",
            ),
            "meta-llama/llama-4-maverick-17b-128e-instruct": LLMConfig(
                max_context_tokens=128000,
                max_output_tokens=32768,
                tokenizer_hub="Quivr/Meta-Llama-3.1-Tokenizer",
            ),
        },
        DefaultModelSuppliers.MISTRAL: {
            "mistral-large": LLMConfig(
                max_context_tokens=128000,
                max_output_tokens=4096,
                tokenizer_hub="Quivr/mistral-tokenizer-v3",
            ),
            "mistral-small": LLMConfig(
                max_context_tokens=128000,
                max_output_tokens=4096,
                tokenizer_hub="Quivr/mistral-tokenizer-v3",
            ),
            "mistral-nemo": LLMConfig(
                max_context_tokens=128000,
                max_output_tokens=4096,
                tokenizer_hub="Quivr/Mistral-Nemo-Instruct-Tokenizer",
            ),
            "codestral": LLMConfig(
                max_context_tokens=32000, tokenizer_hub="Quivr/mistral-tokenizer-v3"
            ),
        },
        DefaultModelSuppliers.GEMINI: {
            "gemini-2.5": LLMConfig(
                max_context_tokens=128000,
                max_output_tokens=4096,
                tokenizer_hub="Quivr/gemini-tokenizer",
            ),
        },
    }

    @classmethod
    def get_supplier_by_model_name(cls, model: str) -> DefaultModelSuppliers | None:
        # Iterate over the suppliers and their models
        for supplier, models in cls._model_defaults.items():
            # Check if the model name or a base part of the model name is in the supplier's models
            for base_model_name in models:
                if model.startswith(base_model_name):
                    return supplier
        # Return None if no supplier matches the model name
        return None

    @classmethod
    def get_llm_model_config(
        cls, supplier: DefaultModelSuppliers, model_name: str
    ) -> Optional[LLMConfig]:
        """Retrieve the LLMConfig (context and tokenizer_hub) for a given supplier and model."""
        supplier_defaults = cls._model_defaults.get(supplier)
        if not supplier_defaults:
            return None

        # Use startswith logic for matching model names
        for key, config in supplier_defaults.items():
            if model_name.startswith(key):
                return config

        return None


class LLMEndpointConfig(QuivrBaseConfig):
    supplier: DefaultModelSuppliers = DefaultModelSuppliers.OPENAI
    model: str = "gpt-4o"
    tokenizer_hub: str | None = None
    llm_base_url: str | None = None
    env_variable_name: str | None = None
    llm_api_key: str | None = None
    max_context_tokens: int = 20000
    max_output_tokens: int = 4096
    temperature: float = 0.3
    streaming: bool = True
    prompt: BasePromptTemplate | None = None

    _FALLBACK_TOKENIZER = "cl100k_base"

    def __hash__(self):
        return hash(
            (
                self.supplier,
                self.model,
                self.tokenizer_hub,
                self.llm_base_url,
                self.env_variable_name,
                self.llm_api_key,
                self.max_context_tokens,
                self.max_output_tokens,
                self.temperature,
                self.streaming,
                repr(self.prompt) if self.prompt is not None else None,
            )
        )

    @property
    def fallback_tokenizer(self) -> str:
        return self._FALLBACK_TOKENIZER

    def __init__(self, **data):
        super().__init__(**data)
        self.set_llm_model_config()
        self.set_api_key()

    def set_api_key(self, force_reset: bool = False):
        if not self.supplier:
            return

        # Check if the corresponding API key environment variable is set
        if force_reset or not self.env_variable_name:
            self.env_variable_name = (
                f"{normalize_to_env_variable_name(self.supplier)}_API_KEY"
            )

        if not self.llm_api_key or force_reset:
            self.llm_api_key = os.getenv(self.env_variable_name)

        if not self.llm_api_key:
            logger.warning(f"The API key for supplier '{self.supplier}' is not set. ")
            logger.warning(
                f"Please set the environment variable: '{self.env_variable_name}'. "
            )

    def set_llm_model_config(self):
        # Automatically set context_length and tokenizer_hub based on the supplier and model
        llm_model_config = LLMModelConfig.get_llm_model_config(
            self.supplier, self.model
        )
        if llm_model_config:
            if llm_model_config.max_context_tokens:
                if self.max_context_tokens > llm_model_config.max_context_tokens:
                    logger.warning(
                        f"Lowering max_context_tokens from {self.max_context_tokens} to {llm_model_config.max_context_tokens}"
                    )
                    self.max_context_tokens = llm_model_config.max_context_tokens

                if self.max_context_tokens < MIN_CONTEXT_TOKENS:
                    logger.error(
                        f"max_context_tokens is too low: {self.max_context_tokens}. "
                    )
                    raise ValueError(
                        f"max_context_tokens is too low: {self.max_context_tokens}. "
                    )
            if llm_model_config.max_output_tokens:
                if self.max_output_tokens > llm_model_config.max_output_tokens:
                    logger.warning(
                        f"Lowering max_output_tokens from {self.max_output_tokens} to {llm_model_config.max_output_tokens}"
                    )
                    self.max_output_tokens = llm_model_config.max_output_tokens

                if self.max_output_tokens < MIN_OUTPUT_TOKENS:
                    logger.error(
                        f"max_output_tokens is too low: {self.max_output_tokens}. "
                    )
                    raise ValueError(
                        f"max_output_tokens is too low: {self.max_output_tokens}. "
                    )

            self.tokenizer_hub = llm_model_config.tokenizer_hub

    def set_llm_model(self, model: str):
        supplier = LLMModelConfig.get_supplier_by_model_name(model)
        if supplier is None:
            raise ValueError(
                f"Cannot find the corresponding supplier for model {model}"
            )
        self.supplier = supplier
        self.model = model

        self.set_llm_model_config()
        self.set_api_key(force_reset=True)

    def set_from_sqlmodel(self, sqlmodel: BaseModel, mapping: Dict[str, str]):
        """
        Set attributes in LLMEndpointConfig from Model attributes using a field mapping.

        :param model_instance: An instance of the Model class.
        :param mapping: A dictionary that maps Model fields to LLMEndpointConfig fields.
                        Example: {"max_input": "max_input_tokens", "env_variable_name": "env_variable_name"}
        """
        for model_field, llm_field in mapping.items():
            if hasattr(sqlmodel, model_field) and hasattr(self, llm_field):
                setattr(self, llm_field, getattr(sqlmodel, model_field))
            else:
                raise AttributeError(
                    f"Invalid mapping: {model_field} or {llm_field} does not exist."
                )


# Cannot use Pydantic v2 field_validator because of conflicts with pydantic v1 still in use in LangChain


class ConditionalEdgeConfig(QuivrBaseConfig):
    routing_function: str
    conditions: Union[list, Dict[Hashable, str]]

    def __init__(self, **data):
        super().__init__(**data)
        self.resolve_special_edges()

    def resolve_special_edges(self):
        """Replace SpecialEdges enum values with their corresponding langgraph values."""

        if isinstance(self.conditions, dict):
            # If conditions is a dictionary, iterate through the key-value pairs
            for key, value in self.conditions.items():
                if value == SpecialEdges.end:
                    self.conditions[key] = END
                elif value == SpecialEdges.start:
                    self.conditions[key] = START
        elif isinstance(self.conditions, list):
            # If conditions is a list, iterate through the values
            for index, value in enumerate(self.conditions):
                if value == SpecialEdges.end:
                    self.conditions[index] = END
                elif value == SpecialEdges.start:
                    self.conditions[index] = START


class NodeConfig(QuivrBaseConfig):
    name: str
    description: str | None = None
    edges: List[str] | None = None
    conditional_edge: ConditionalEdgeConfig | None = None
    tools_configs: List[Dict[str, Any]] | None = None

    # Store validated node-specific configs
    validated_configs: Dict[str, QuivrBaseConfig] = {}

    class Config:
        extra = "allow"  # Allow additional fields for node-specific configs

    @field_serializer("validated_configs")
    def serialize_validated_configs(
        self, value: Dict[str, QuivrBaseConfig]
    ) -> Dict[str, Any]:
        """Custom serializer for validated_configs field."""
        if not value:
            return {}

        serialized_configs = {}
        for key, config in value.items():
            if hasattr(config, "model_dump"):
                # If it's a Pydantic model, use its model_dump method
                serialized_configs[key] = config.model_dump()
            else:
                # If it's raw data, keep as is
                serialized_configs[key] = config
        return serialized_configs

    def __init__(self, **data):
        # Extract and validate node-specific configs BEFORE calling super().__init__
        node_configs = {}
        validated_configs = {}

        # Find all config fields (ending with '_config')
        for key, value in list(data.items()):
            if key.endswith("_config") and key not in ["conditional_edge"]:
                # Remove from data to avoid Pydantic validation issues
                config_data = data.pop(key)
                node_configs[key] = config_data

                # Validate against registered config type
                if key in NODE_CONFIG_TYPES:
                    config_type = NODE_CONFIG_TYPES[key]
                    try:
                        validated_config = config_type.model_validate(config_data)
                        validated_configs[key] = validated_config
                        logger.debug(f"Validated {key} for node config")
                    except Exception as e:
                        raise ValueError(
                            f"Invalid {key} in node '{data.get('name', 'unknown')}': {e}"
                        )
                else:
                    logger.warning(f"Unknown config type '{key}' - storing as raw data")
                    validated_configs[key] = config_data

        # Store validated configs
        data["validated_configs"] = validated_configs

        super().__init__(**data)
        self._validate_tools()
        self.resolve_special_edges_in_name_and_edges()

    def get_node_config(self, config_type: Type[T], config_key: str) -> Optional[T]:
        """Get a validated config of specific type."""
        config = self.validated_configs.get(config_key)
        if config and isinstance(config, config_type):
            return config
        return None

    def has_config(self, config_key: str) -> bool:
        """Check if node has a specific config."""
        return config_key in self.validated_configs

    def resolve_special_edges_in_name_and_edges(self):
        """Replace SpecialEdges enum values in name and edges with corresponding langgraph values."""
        if self.name == SpecialEdges.start:
            self.name = START
        elif self.name == SpecialEdges.end:
            self.name = END

        if self.edges:
            for i, edge in enumerate(self.edges):
                if edge == SpecialEdges.start:
                    self.edges[i] = START
                elif edge == SpecialEdges.end:
                    self.edges[i] = END

    def _validate_tools(self):
        """Validate tools based on the configuration."""
        if self.tools_configs:
            for tool_config in self.tools_configs:
                # Make a copy to avoid modifying the original
                tool_name = tool_config.get("name")
                if not tool_name:
                    logger.error("Tool config has no 'name'")
                    raise ValueError("Tool config has no 'name'")

                # Check if tool exists in the registry
                if not tool_registry.has_item(tool_name):
                    logger.error(f"Tool '{tool_name}' not found in registry")
                    raise ValueError(f"Tool '{tool_name}' not found in registry")


class DefaultWorkflow(str, Enum):
    RAG = "rag"
    CHAT_WITH_LLM = "chat_with_llm"

    @property
    def nodes(self) -> List[NodeConfig]:
        # Mapping of workflow types to their default node configurations
        workflows = {
            self.RAG: [
                NodeConfig(name=START, edges=["filter_history"]),
                NodeConfig(name="filter_history", edges=["rewrite"]),
                NodeConfig(name="rewrite", edges=["retrieve"]),
                NodeConfig(name="retrieve", edges=["generate_rag"]),
                NodeConfig(name="generate_rag", edges=[END]),
            ],
            self.CHAT_WITH_LLM: [
                NodeConfig(name=START, edges=["filter_history"]),
                NodeConfig(name="filter_history", edges=["generate_chat_llm"]),
                NodeConfig(name="generate_chat_llm", edges=[END]),
            ],
        }
        return workflows[self]


class WorkflowConfig(QuivrBaseConfig):
    name: str | None = None
    nodes: List[NodeConfig] = []

    def __init__(self, **data):
        super().__init__(**data)
        self.check_first_node_is_start()

    def check_first_node_is_start(self):
        if self.nodes and self.nodes[0].name != START:
            raise ValueError(f"The first node should be a {SpecialEdges.start} node")


class CitationConfig(QuivrBaseConfig):
    max_files: int = 20


class RetrievalConfig(QuivrBaseConfig):
    citation_config: CitationConfig = CitationConfig()
    reranker_config: RerankerConfig = RerankerConfig()
    retriever_config: RetrieverConfig = RetrieverConfig()
    llm_config: LLMEndpointConfig = LLMEndpointConfig()
    filter_history_config: FilterHistoryConfig = FilterHistoryConfig()
    prompt_config: PromptConfig = PromptConfig()
    workflow_config: WorkflowConfig = WorkflowConfig(nodes=DefaultWorkflow.RAG.nodes)

    def __init__(self, **data):
        super().__init__(**data)
        self.llm_config.set_api_key(force_reset=True)


class ParserConfig(QuivrBaseConfig):
    splitter_config: SplitterConfig = SplitterConfig()
    megaparse_config: MegaparseConfig = MegaparseConfig()


class IngestionConfig(QuivrBaseConfig):
    parser_config: ParserConfig = ParserConfig()


class AssistantConfig(QuivrBaseConfig):
    retrieval_config: RetrievalConfig = RetrievalConfig()
    ingestion_config: IngestionConfig = IngestionConfig()


# Registry mapping config field names to their Pydantic types
NODE_CONFIG_TYPES: Dict[str, Type[QuivrBaseConfig]] = {
    "llm_config": LLMEndpointConfig,
    "reranker_config": RerankerConfig,
    "retriever_config": RetrieverConfig,
    "prompt_config": PromptConfig,
    "filter_history_config": FilterHistoryConfig,
}


def register_node_config_type(config_name: str, config_type: Type[QuivrBaseConfig]):
    """Register a new node config type for validation."""
    NODE_CONFIG_TYPES[config_name] = config_type
