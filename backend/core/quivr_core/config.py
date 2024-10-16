import os
from enum import Enum
from typing import Dict, List, Optional
from uuid import UUID

from megaparse.config import MegaparseConfig
from sqlmodel import SQLModel

from quivr_core.base_config import QuivrBaseConfig
from quivr_core.processor.splitter import SplitterConfig
from quivr_core.prompts import CustomPromptsModel


class BrainConfig(QuivrBaseConfig):
    brain_id: UUID | None = None
    name: str

    @property
    def id(self) -> UUID | None:
        return self.brain_id


class DefaultRerankers(str, Enum):
    """
    Enum representing the default API-based reranker suppliers supported by the application.

    This enum defines the various reranker providers that can be used in the system.
    Each enum value corresponds to a specific supplier's identifier and has an
    associated default model.

    Attributes:
        COHERE (str): Represents Cohere AI as a reranker supplier.
        JINA (str): Represents Jina AI as a reranker supplier.

    Methods:
        default_model (property): Returns the default model for the selected supplier.
    """

    COHERE = "cohere"
    JINA = "jina"

    @property
    def default_model(self) -> str:
        """
        Get the default model for the selected reranker supplier.

        This property method returns the default model associated with the current
        reranker supplier (COHERE or JINA).

        Returns:
            str: The name of the default model for the selected supplier.

        Raises:
            KeyError: If the current enum value doesn't have a corresponding default model.
        """
        # Mapping of suppliers to their default models
        return {
            self.COHERE: "rerank-multilingual-v3.0",
            self.JINA: "jina-reranker-v2-base-multilingual",
        }[self]


class DefaultModelSuppliers(str, Enum):
    """
    Enum representing the default model suppliers supported by the application.

    This enum defines the various AI model providers that can be used as sources
    for LLMs in the system. Each enum value corresponds to a specific
    supplier's identifier.

    Attributes:
        OPENAI (str): Represents OpenAI as a model supplier.
        AZURE (str): Represents Azure (Microsoft) as a model supplier.
        ANTHROPIC (str): Represents Anthropic as a model supplier.
        META (str): Represents Meta as a model supplier.
        MISTRAL (str): Represents Mistral AI as a model supplier.
        GROQ (str): Represents Groq as a model supplier.
    """

    OPENAI = "openai"
    AZURE = "azure"
    ANTHROPIC = "anthropic"
    META = "meta"
    MISTRAL = "mistral"
    GROQ = "groq"


class LLMConfig(QuivrBaseConfig):
    context: int | None = None
    tokenizer_hub: str | None = None


class LLMModelConfig:
    _model_defaults: Dict[DefaultModelSuppliers, Dict[str, LLMConfig]] = {
        DefaultModelSuppliers.OPENAI: {
            "gpt-4o": LLMConfig(context=128000, tokenizer_hub="Xenova/gpt-4o"),
            "gpt-4o-mini": LLMConfig(context=128000, tokenizer_hub="Xenova/gpt-4o"),
            "gpt-4-turbo": LLMConfig(context=128000, tokenizer_hub="Xenova/gpt-4"),
            "gpt-4": LLMConfig(context=8192, tokenizer_hub="Xenova/gpt-4"),
            "gpt-3.5-turbo": LLMConfig(
                context=16385, tokenizer_hub="Xenova/gpt-3.5-turbo"
            ),
            "text-embedding-3-large": LLMConfig(
                context=8191, tokenizer_hub="Xenova/text-embedding-ada-002"
            ),
            "text-embedding-3-small": LLMConfig(
                context=8191, tokenizer_hub="Xenova/text-embedding-ada-002"
            ),
            "text-embedding-ada-002": LLMConfig(
                context=8191, tokenizer_hub="Xenova/text-embedding-ada-002"
            ),
        },
        DefaultModelSuppliers.ANTHROPIC: {
            "claude-3-5-sonnet": LLMConfig(
                context=200000, tokenizer_hub="Xenova/claude-tokenizer"
            ),
            "claude-3-opus": LLMConfig(
                context=200000, tokenizer_hub="Xenova/claude-tokenizer"
            ),
            "claude-3-sonnet": LLMConfig(
                context=200000, tokenizer_hub="Xenova/claude-tokenizer"
            ),
            "claude-3-haiku": LLMConfig(
                context=200000, tokenizer_hub="Xenova/claude-tokenizer"
            ),
            "claude-2-1": LLMConfig(
                context=200000, tokenizer_hub="Xenova/claude-tokenizer"
            ),
            "claude-2-0": LLMConfig(
                context=100000, tokenizer_hub="Xenova/claude-tokenizer"
            ),
            "claude-instant-1-2": LLMConfig(
                context=100000, tokenizer_hub="Xenova/claude-tokenizer"
            ),
        },
        DefaultModelSuppliers.META: {
            "llama-3.1": LLMConfig(
                context=128000, tokenizer_hub="Xenova/Meta-Llama-3.1-Tokenizer"
            ),
            "llama-3": LLMConfig(
                context=8192, tokenizer_hub="Xenova/llama3-tokenizer-new"
            ),
            "llama-2": LLMConfig(context=4096, tokenizer_hub="Xenova/llama2-tokenizer"),
            "code-llama": LLMConfig(
                context=16384, tokenizer_hub="Xenova/llama-code-tokenizer"
            ),
        },
        DefaultModelSuppliers.GROQ: {
            "llama-3.1": LLMConfig(
                context=128000, tokenizer_hub="Xenova/Meta-Llama-3.1-Tokenizer"
            ),
            "llama-3": LLMConfig(
                context=8192, tokenizer_hub="Xenova/llama3-tokenizer-new"
            ),
            "llama-2": LLMConfig(context=4096, tokenizer_hub="Xenova/llama2-tokenizer"),
            "code-llama": LLMConfig(
                context=16384, tokenizer_hub="Xenova/llama-code-tokenizer"
            ),
        },
        DefaultModelSuppliers.MISTRAL: {
            "mistral-large": LLMConfig(
                context=128000, tokenizer_hub="Xenova/mistral-tokenizer-v3"
            ),
            "mistral-small": LLMConfig(
                context=128000, tokenizer_hub="Xenova/mistral-tokenizer-v3"
            ),
            "mistral-nemo": LLMConfig(
                context=128000, tokenizer_hub="Xenova/Mistral-Nemo-Instruct-Tokenizer"
            ),
            "codestral": LLMConfig(
                context=32000, tokenizer_hub="Xenova/mistral-tokenizer-v3"
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
    """
    Configuration class for Large Language Models (LLM) endpoints.

    This class defines the settings and parameters for interacting with various LLM providers.
    It includes configuration for the model, API keys, token limits, and other relevant settings.

    Attributes:
        supplier (DefaultModelSuppliers): The LLM provider (default: OPENAI).
        model (str): The specific model to use (default: "gpt-3.5-turbo-0125").
        context_length (int | None): The maximum context length for the model.
        tokenizer_hub (str | None): The tokenizer to use for this model.
        llm_base_url (str | None): Base URL for the LLM API.
        env_variable_name (str): Name of the environment variable for the API key.
        llm_api_key (str | None): The API key for the LLM provider.
        max_input_tokens (int): Maximum number of input tokens sent to the LLM (default: 2000).
        max_output_tokens (int): Maximum number of output tokens returned by the LLM (default: 2000).
        temperature (float): Temperature setting for text generation (default: 0.7).
        streaming (bool): Whether to use streaming for responses (default: True).
        prompt (CustomPromptsModel | None): Custom prompt configuration.
    """

    supplier: DefaultModelSuppliers = DefaultModelSuppliers.OPENAI
    model: str = "gpt-3.5-turbo-0125"
    context_length: int | None = None
    tokenizer_hub: str | None = None
    llm_base_url: str | None = None
    env_variable_name: str = f"{supplier.upper()}_API_KEY"
    llm_api_key: str | None = None
    max_input_tokens: int = 2000
    max_output_tokens: int = 2000
    temperature: float = 0.7
    streaming: bool = True
    prompt: CustomPromptsModel | None = None

    _FALLBACK_TOKENIZER = "cl100k_base"

    @property
    def fallback_tokenizer(self) -> str:
        """
        Get the fallback tokenizer.

        Returns:
            str: The name of the fallback tokenizer.
        """
        return self._FALLBACK_TOKENIZER

    def __init__(self, **data):
        """
        Initialize the LLMEndpointConfig.

        This method sets up the initial configuration, including setting the LLM model
        config and API key.

        """
        super().__init__(**data)
        self.set_llm_model_config()
        self.set_api_key()

    def set_api_key(self, force_reset: bool = False):
        """
        Set the API key for the LLM provider.

        This method attempts to set the API key from the environment variable.
        If the key is not found, it raises a ValueError.

        Args:
            force_reset (bool): If True, forces a reset of the API key even if already set.

        Raises:
            ValueError: If the API key is not set in the environment.
        """
        if not self.llm_api_key or force_reset:
            self.llm_api_key = os.getenv(self.env_variable_name)

        if not self.llm_api_key:
            raise ValueError(
                f"The API key for supplier '{self.supplier}' is not set. "
                f"Please set the environment variable: {self.env_variable_name}"
            )

    def set_llm_model_config(self):
        """
        Set the LLM model configuration.

        This method automatically sets the context_length and tokenizer_hub
        based on the current supplier and model.
        """
        llm_model_config = LLMModelConfig.get_llm_model_config(
            self.supplier, self.model
        )
        if llm_model_config:
            self.context_length = llm_model_config.context
            self.tokenizer_hub = llm_model_config.tokenizer_hub

    def set_llm_model(self, model: str):
        """
        Set the LLM model and update related configurations.

        This method updates the supplier and model based on the provided model name,
        then updates the model config and API key accordingly.

        Args:
            model (str): The name of the model to set.

        Raises:
            ValueError: If no corresponding supplier is found for the given model.
        """
        supplier = LLMModelConfig.get_supplier_by_model_name(model)
        if supplier is None:
            raise ValueError(
                f"Cannot find the corresponding supplier for model {model}"
            )
        self.supplier = supplier
        self.model = model

        self.set_llm_model_config()
        self.set_api_key(force_reset=True)

    def set_from_sqlmodel(self, sqlmodel: SQLModel, mapping: Dict[str, str]):
        """
        Set attributes in LLMEndpointConfig from SQLModel attributes using a field mapping.

        This method allows for dynamic setting of LLMEndpointConfig attributes based on
        a provided SQLModel instance and a mapping dictionary.

        Args:
            sqlmodel (SQLModel): An instance of the SQLModel class.
            mapping (Dict[str, str]): A dictionary that maps SQLModel fields to LLMEndpointConfig fields.
                Example: {"max_input": "max_input_tokens", "env_variable_name": "env_variable_name"}

        Raises:
            AttributeError: If any field in the mapping doesn't exist in either the SQLModel or LLMEndpointConfig.
        """
        for model_field, llm_field in mapping.items():
            if hasattr(sqlmodel, model_field) and hasattr(self, llm_field):
                setattr(self, llm_field, getattr(sqlmodel, model_field))
            else:
                raise AttributeError(
                    f"Invalid mapping: {model_field} or {llm_field} does not exist."
                )


# Cannot use Pydantic v2 field_validator because of conflicts with pydantic v1 still in use in LangChain
class RerankerConfig(QuivrBaseConfig):
    """
    Configuration class for reranker models.

    This class defines the settings for reranker models used in the application,
    including the supplier, model, and API key information.

    Attributes:
        supplier (DefaultRerankers | None): The reranker supplier (e.g., COHERE).
        model (str | None): The specific reranker model to use.
        top_n (int): The number of top chunks returned by the reranker (default: 5).
        api_key (str | None): The API key for the reranker service.
    """

    supplier: DefaultRerankers | None = None
    model: str | None = None
    top_n: int = 5
    api_key: str | None = None

    def __init__(self, **data):
        """
        Initialize the RerankerConfig.
        """
        super().__init__(**data)
        self.validate_model()

    def validate_model(self):
        """
        Validate and set up the reranker model configuration.

        This method ensures that a model is set (using the default if not provided)
        and that the necessary API key is available in the environment.

        Raises:
            ValueError: If the required API key is not set in the environment.
        """
        if self.model is None and self.supplier is not None:
            self.model = self.supplier.default_model

        if self.supplier:
            api_key_var = f"{self.supplier.upper()}_API_KEY"
            self.api_key = os.getenv(api_key_var)

            if self.api_key is None:
                raise ValueError(
                    f"The API key for supplier '{self.supplier}' is not set. "
                    f"Please set the environment variable: {api_key_var}"
                )


class NodeConfig(QuivrBaseConfig):
    """
    Configuration class for a node in an AI assistant workflow.

    This class represents a single node in a workflow configuration,
    defining its name and connections to other nodes.

    Attributes:
        name (str): The name of the node.
        edges (List[str]): List of names of other nodes this node links to.
    """

    name: str
    edges: List[str]


class WorkflowConfig(QuivrBaseConfig):
    """
    Configuration class for an AI assistant workflow.

    This class represents the entire workflow configuration,
    consisting of multiple interconnected nodes.

    Attributes:
        name (str): The name of the workflow.
        nodes (List[NodeConfig]): List of nodes in the workflow.
    """

    name: str
    nodes: List[NodeConfig]


class RetrievalConfig(QuivrBaseConfig):
    """
    Configuration class for the retrieval phase of a RAG assistant.

    This class defines the settings for the retrieval process,
    including reranker and LLM configurations, as well as various limits and prompts.

    Attributes:
        workflow_config (WorkflowConfig | None): Configuration for the workflow.
        reranker_config (RerankerConfig): Configuration for the reranker.
        llm_config (LLMEndpointConfig): Configuration for the LLM endpoint.
        max_history (int): Maximum number of past conversation turns to pass to the LLM as context (default: 10).
        max_files (int): Maximum number of files to process (default: 20).
        prompt (str | None): Custom prompt for the retrieval process.
    """
    
    workflow_config: WorkflowConfig | None = None
    reranker_config: RerankerConfig = RerankerConfig()
    llm_config: LLMEndpointConfig = LLMEndpointConfig()
    max_history: int = 10
    max_files: int = 20
    prompt: str | None = None


class ParserConfig(QuivrBaseConfig):
    """
    Configuration class for the parser.

    This class defines the settings for the parsing process,
    including configurations for the text splitter and Megaparse.

    Attributes:
        splitter_config (SplitterConfig): Configuration for the text splitter.
        megaparse_config (MegaparseConfig): Configuration for Megaparse.
    """

    splitter_config: SplitterConfig = SplitterConfig()
    megaparse_config: MegaparseConfig = MegaparseConfig()


class IngestionConfig(QuivrBaseConfig):
    """
    Configuration class for the data ingestion process.

    This class defines the settings for the data ingestion process,
    including the parser configuration.

    Attributes:
        parser_config (ParserConfig): Configuration for the parser.
    """

    parser_config: ParserConfig = ParserConfig()


class AssistantConfig(QuivrBaseConfig):
    """
    Configuration class for an AI assistant.

    This class defines the overall configuration for an AI assistant,
    including settings for retrieval and ingestion processes.

    Attributes:
        retrieval_config (RetrievalConfig): Configuration for the retrieval process.
        ingestion_config (IngestionConfig): Configuration for the ingestion process.
    """

    retrieval_config: RetrievalConfig = RetrievalConfig()
    ingestion_config: IngestionConfig = IngestionConfig()