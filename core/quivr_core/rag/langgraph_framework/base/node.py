import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Tuple, Type, TypeVar, cast
from pydantic import BaseModel

from quivr_core.rag.langgraph_framework.base.extractors import ConfigExtractor
from quivr_core.rag.langgraph_framework.base.graph_config import BaseGraphConfig
from quivr_core.rag.langgraph_framework.base.utils import compute_config_hash
from quivr_core.rag.langgraph_framework.services.service_container import (
    ServiceContainer,
)

logger = logging.getLogger("quivr_core")

T = TypeVar("T", bound=BaseModel)
S = TypeVar("S")  # For services


def extract_config_from_runnable(config: Optional[BaseGraphConfig]) -> Dict[str, Any]:
    """Extract custom configuration from LangGraph's RunnableConfig format."""
    if not config:
        return {}
    return config.get("configurable", {})


class BaseNode(ABC):
    """
    Abstract base class for all LangGraph nodes with dependency injection support.
    """

    NODE_NAME: str = "base_node"
    _node_metadata: Optional[Dict[str, Any]] = None

    def __init__(
        self,
        config_extractor: Optional[ConfigExtractor] = None,
        node_name: Optional[str] = None,
        service_container: Optional[ServiceContainer] = None,
    ):
        """Initialize the base node."""
        self.node_name = node_name or self.NODE_NAME
        self.logger = logging.getLogger(f"quivr_core.nodes.{self.node_name}")
        self.config_extractor = config_extractor
        self.service_container = service_container or ServiceContainer()
        # Cache for config hashes to detect changes (keyed by (config_type, node_name))
        self._config_hashes: Dict[Tuple[Type[BaseModel], str], str] = {}

    @property
    def name(self):
        return self.node_name

    def get_config(
        self, config_type: Type[T], config: Optional[BaseGraphConfig] = None
    ) -> T:
        """
        Extract a specific configuration type with change detection and node-specific overrides.

        Args:
            config_type: The type of config to extract
            config: The graph config to extract from

        Returns:
            config_instance: The extracted config (with node-specific overrides if any)
        """
        if not self.config_extractor or not config:
            default_config = config_type()
            current_hash = compute_config_hash(default_config)

            cache_key = (config_type, self.node_name)

            # Update the cached hash
            self._config_hashes[cache_key] = current_hash

            return default_config

        # Extract config with node-specific overrides
        extracted_config = cast(
            T, self.config_extractor.extract(config, config_type, self.node_name)
        )
        current_hash = compute_config_hash(extracted_config)

        # Check if this is a new config or if it has changed
        cache_key = (config_type, self.node_name)

        # Update the cached hash
        self._config_hashes[cache_key] = current_hash

        return extracted_config

    def get_service(
        self,
        service_type: Type[S],
        config: Optional[Any] = None,
        runtime_context: Optional[Dict[str, Any]] = None,
        use_cache: bool = True,
    ) -> S:
        """Get a service instance from the container."""
        return self.service_container.get_service(
            service_type, config, runtime_context, use_cache=use_cache
        )

    @abstractmethod
    def validate_input_state(self, state) -> None:
        """Validate input state. Override in subclasses for specific validation."""
        pass

    @abstractmethod
    def validate_output_state(self, state) -> None:
        """Validate output state. Override in subclasses for specific validation."""
        pass

    def handle_error(self, error: Exception, state):
        """Handle errors during execution."""
        error_msg = f"Error in {self.node_name}: {str(error)}"

        if hasattr(state, "with_error") and callable(getattr(state, "with_error")):
            return state.with_error(error_msg)
        elif isinstance(state, dict):
            return {**state, "error": error_msg, "node_error": self.node_name}
        else:
            self.logger.error(f"Could not add error info to state: {error_msg}")
            return state

    async def __call__(self, state, config: Optional[BaseGraphConfig] = None):
        """LangGraph-compatible interface."""
        try:
            self.validate_input_state(state)
            self.logger.debug(f"Executing {self.node_name}")

            result = await self.execute(state, config)

            self.validate_output_state(result)
            self.logger.debug(f"Completed {self.node_name}")

            return result

        except Exception as e:
            self.logger.error(f"Error in {self.node_name}: {str(e)}", exc_info=True)
            raise

    @abstractmethod
    async def execute(self, state, config: Optional[BaseGraphConfig] = None):
        """Execute the core node logic."""
        pass
