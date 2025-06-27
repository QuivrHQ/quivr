"""Mock nodes for testing."""

from typing import Optional
from pydantic import BaseModel

from quivr_core.rag.langgraph_framework.base.node import BaseNode
from quivr_core.rag.langgraph_framework.base.graph_config import BaseGraphConfig
from quivr_core.rag.langgraph_framework.base.exceptions import NodeValidationError


class MockConfig(BaseModel):
    """Mock configuration for testing."""

    test_param: str = "default_value"
    numeric_param: int = 42


class MockNode(BaseNode):
    """Simple mock node for testing."""

    NODE_NAME = "mock_node"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.executed = False
        self.execution_count = 0
        self.last_state = None
        self.last_config = None

    def validate_input_state(self, state) -> None:
        """Mock input validation."""
        if hasattr(state, "invalid") and state.invalid:
            raise ValueError("Invalid input state")
        if isinstance(state, dict) and state.get("invalid_input"):
            raise ValueError("Invalid input state")

    def validate_output_state(self, state) -> None:
        """Mock output validation."""
        if hasattr(state, "invalid_output") and state.invalid_output:
            raise ValueError("Invalid output state")
        if isinstance(state, dict) and state.get("invalid_output"):
            raise ValueError("Invalid output state")

    async def execute(self, state, config: Optional[BaseGraphConfig] = None):
        """Mock execution."""
        self.executed = True
        self.execution_count += 1
        self.last_state = state
        self.last_config = config

        # Return modified state
        if isinstance(state, dict):
            return {**state, "processed_by": self.node_name}
        else:
            # For non-dict states, just return as-is
            return state


class ValidationErrorMockNode(BaseNode):
    """Mock node that raises NodeValidationError for testing."""

    NODE_NAME = "validation_error_mock_node"

    def validate_input_state(self, state) -> None:
        """Raises NodeValidationError if state has validation_error flag."""
        if isinstance(state, dict) and state.get("validation_error"):
            raise NodeValidationError("Validation failed")

    def validate_output_state(self, state) -> None:
        pass

    async def execute(self, state, config: Optional[BaseGraphConfig] = None):
        """Simple execution."""
        return {"executed": True}


class FailingMockNode(BaseNode):
    """Mock node that always fails for error testing."""

    NODE_NAME = "failing_mock_node"

    def validate_input_state(self, state) -> None:
        pass

    def validate_output_state(self, state) -> None:
        pass

    async def execute(self, state, config: Optional[BaseGraphConfig] = None):
        """Always fails."""
        raise RuntimeError("Mock execution failure")


class AsyncMockNode(BaseNode):
    """Mock node for async testing."""

    NODE_NAME = "async_mock_node"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.async_executed = False

    def validate_input_state(self, state) -> None:
        pass

    def validate_output_state(self, state) -> None:
        pass

    async def execute(self, state, config: Optional[BaseGraphConfig] = None):
        """Async execution."""
        # Simulate async work
        import asyncio

        await asyncio.sleep(0.01)

        self.async_executed = True
        return {"async_result": True}
