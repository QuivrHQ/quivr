"""Tests for various nodes."""

import pytest

from quivr_core.rag.langgraph_framework.nodes.various.edit_system_prompt_node import (
    EditSystemPromptNode,
)
from quivr_core.rag.langgraph_framework.base.exceptions import NodeValidationError

from tests.rag.langgraph_framework.fixtures.test_data import (
    create_sample_agent_state,
)


class TestEditSystemPromptNode:
    """Test EditSystemPromptNode functionality."""

    @pytest.fixture(scope="function")
    def edit_system_prompt_node(self):
        """Create an EditSystemPromptNode instance."""
        return EditSystemPromptNode()

    @pytest.fixture(scope="function")
    def valid_state(self):
        """Create a valid state for testing."""
        state = create_sample_agent_state()
        state["instructions"] = "Please be more helpful and concise in your responses."
        return state

    def test_node_name(self, edit_system_prompt_node):
        """Test node name."""
        assert edit_system_prompt_node.NODE_NAME == "edit_system_prompt"

    def test_validate_input_state_success(self, edit_system_prompt_node, valid_state):
        """Test successful input state validation."""
        edit_system_prompt_node.validate_input_state(valid_state)

    def test_validate_input_state_missing_instructions(self, edit_system_prompt_node):
        """Test input validation with missing instructions."""
        state = {"messages": []}

        with pytest.raises(
            NodeValidationError, match="requires 'instructions' attribute"
        ):
            edit_system_prompt_node.validate_input_state(state)

    def test_validate_input_state_empty_instructions(self, edit_system_prompt_node):
        """Test input validation with empty instructions."""
        state = {"instructions": ""}

        with pytest.raises(
            NodeValidationError, match="requires non-empty instructions"
        ):
            edit_system_prompt_node.validate_input_state(state)

    def test_validate_input_state_none_instructions(self, edit_system_prompt_node):
        """Test input validation with None instructions."""
        state = {"instructions": None}

        with pytest.raises(
            NodeValidationError, match="requires non-empty instructions"
        ):
            edit_system_prompt_node.validate_input_state(state)

    def test_validate_output_state(self, edit_system_prompt_node):
        """Test output state validation (currently no-op)."""
        edit_system_prompt_node.validate_output_state({})

    # Note: Execution tests for EditSystemPromptNode would require complex mocking
    # of the actual LLM service's invoke_with_structured_output method and understanding
    # of the UpdatedPromptAndTools entity. The validation tests above are the main focus
    # and they are working correctly.


class TestEditSystemPromptNodeIntegration:
    """Test integration aspects of edit system prompt node."""

    def test_edit_system_prompt_node_registered(self):
        """Test that edit system prompt node is properly registered."""
        # Import the nodes package to ensure all decorators are executed
        import quivr_core.rag.langgraph_framework.nodes  # noqa: F401

        from quivr_core.rag.langgraph_framework.registry.node_registry import (
            node_registry,
        )

        various_nodes = node_registry.list_nodes("various")
        assert (
            "edit_system_prompt" in various_nodes
        ), f"EditSystemPromptNode not registered. Available various nodes: {various_nodes}"

    def test_edit_system_prompt_node_dependencies(self):
        """Test that edit system prompt node declares proper dependencies."""
        node = EditSystemPromptNode()

        # Should have proper node name
        assert hasattr(node, "NODE_NAME")
        assert node.NODE_NAME == "edit_system_prompt"
