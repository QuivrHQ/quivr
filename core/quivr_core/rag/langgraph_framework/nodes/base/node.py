import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Tuple, Type, TypeVar, cast
from pydantic import BaseModel

from quivr_core.rag.langgraph_framework.nodes.base.extractors import ConfigExtractor
from quivr_core.rag.langgraph_framework.nodes.base.graph_config import BaseGraphConfig
from quivr_core.rag.langgraph_framework.nodes.base.exceptions import NodeValidationError

logger = logging.getLogger("quivr_core")

T = TypeVar("T", bound=BaseModel)


def extract_config_from_runnable(config: Optional[BaseGraphConfig]) -> Dict[str, Any]:
    """Extract custom configuration from LangGraph's RunnableConfig format."""
    if not config:
        return {}
    return config.get("configurable", {})


class BaseNode(ABC):
    """
    Abstract base class for all LangGraph nodes.
    """

    NODE_NAME: str = "base_node"
    CONFIG_TYPES: Tuple[Type[BaseModel], ...] = ()

    def __init__(
        self,
        config_extractor: Optional[ConfigExtractor] = None,
        node_name: Optional[str] = None,
    ):
        """Initialize the base node."""
        self.node_name = node_name or self.NODE_NAME
        self.logger = logging.getLogger(f"quivr_core.nodes.{self.node_name}")
        self.config_extractor = config_extractor

    @property
    def name(self):
        return self.node_name

    def get_config(
        self, config_type: Type[T], config: Optional[BaseGraphConfig] = None
    ) -> T:
        """
        Extract a specific configuration type with proper typing.
        """
        if not self.config_extractor or not config:
            return config_type()

        return cast(T, self.config_extractor.extract(config, config_type))

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

        except NodeValidationError:
            raise
        except Exception as e:
            self.logger.error(f"Error in {self.node_name}: {str(e)}", exc_info=True)
            return self.handle_error(e, state)

    @abstractmethod
    async def execute(self, state, config: Optional[BaseGraphConfig] = None):
        """Execute the core node logic."""
        pass
