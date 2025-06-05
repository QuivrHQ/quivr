import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, TypeVar
from quivr_core.rag.langgraph_framework.nodes.base.extractors import ConfigExtractor
from quivr_core.rag.langgraph_framework.nodes.base.base_state import BaseState

logger = logging.getLogger("quivr_core")

# Define generic types for the state
InputStateT = TypeVar("InputStateT", bound=BaseState)
OutputStateT = TypeVar("OutputStateT", bound=BaseState)


class NodeValidationError(Exception):
    """Raised when node state validation fails."""

    pass


class NodeExecutionError(Exception):
    """Raised when node execution fails."""

    pass


def extract_config_from_runnable(config: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Extract custom configuration from LangGraph's RunnableConfig format."""
    if not config:
        return {}
    return config.get("configurable", {})


class BaseNode(ABC):
    """
    Abstract base class for all LangGraph nodes.

    Nodes work with state objects and validate required attributes at runtime.
    The actual state type is determined by the graph configuration at runtime.
    """

    NODE_NAME: str = "base_node"

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

    @abstractmethod
    def validate_input_state(self, state) -> None:
        """
        Validate input state. Override in subclasses for specific validation.

        Args:
            state: The input state object (type determined at runtime)
        """
        pass

    @abstractmethod
    def validate_output_state(self, state) -> None:
        """
        Validate output state. Override in subclasses for specific validation.

        Args:
            state: The output state object (type determined at runtime)
        """
        pass

    def handle_error(self, error: Exception, state):
        """
        Handle errors during execution.

        Args:
            error: The exception that occurred
            state: The input state object

        Returns:
            The state object, potentially with error information added
        """
        error_msg = f"Error in {self.node_name}: {str(error)}"

        # Try to add error info if state supports it
        if hasattr(state, "with_error") and callable(getattr(state, "with_error")):
            return state.with_error(error_msg)
        elif isinstance(state, dict):
            return {**state, "error": error_msg, "node_error": self.node_name}
        else:
            # Log the error and return original state
            self.logger.error(f"Could not add error info to state: {error_msg}")
            return state

    def get_config(self, config: Optional[Dict[str, Any]]):
        """
        Get configuration using the injected config extractor.
        Returns None if no extractor is provided.
        """
        if not self.config_extractor or not config:
            return None

        return self.config_extractor(config)

    async def __call__(self, state, config: Optional[Dict[str, Any]] = None):
        """
        LangGraph-compatible interface. Validates input, executes node, validates output.

        Args:
            state: The input state object (type determined at runtime)
            config: Optional configuration dictionary

        Returns:
            The updated state object
        """
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
    async def execute(self, state, config: Optional[Dict[str, Any]] = None):
        """
        Execute the core node logic. Must be implemented by subclasses.

        Args:
            state: The input state object (type determined at runtime)
            config: Optional configuration dictionary

        Returns:
            The updated state object
        """
        pass
