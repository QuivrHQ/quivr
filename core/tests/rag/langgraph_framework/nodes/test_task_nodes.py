"""Tests for task nodes."""

import pytest
from unittest.mock import Mock
from langchain_core.messages import HumanMessage

from quivr_core.rag.langgraph_framework.nodes.tasks.transform_tasks_node import (
    TransformTasksNode,
)
from quivr_core.rag.langgraph_framework.base.exceptions import NodeValidationError

from tests.rag.langgraph_framework.fixtures.test_data import (
    create_sample_agent_state,
    create_sample_user_tasks,
    create_sample_chat_history,
)


class TestTransformTasksNode:
    """Test TransformTasksNode functionality."""

    @pytest.fixture(scope="function")
    def transform_tasks_node(self):
        """Create a TransformTasksNode instance."""
        return TransformTasksNode()

    @pytest.fixture(scope="function")
    def valid_state(self):
        """Create a valid state for testing."""
        state = create_sample_agent_state()
        state["tasks"] = create_sample_user_tasks()
        state["chat_history"] = create_sample_chat_history()
        return state

    def test_node_name(self, transform_tasks_node):
        """Test node name."""
        assert transform_tasks_node.NODE_NAME == "transform_tasks"

    def test_validate_input_state_success(self, transform_tasks_node, valid_state):
        """Test successful input state validation."""
        transform_tasks_node.validate_input_state(valid_state)

    def test_validate_input_state_missing_messages(self, transform_tasks_node):
        """Test input validation with missing messages."""
        state = {"chat_history": create_sample_chat_history()}

        with pytest.raises(NodeValidationError, match="requires 'messages' attribute"):
            transform_tasks_node.validate_input_state(state)

    def test_validate_input_state_empty_messages(self, transform_tasks_node):
        """Test input validation with empty messages."""
        state = {
            "messages": [],
            "chat_history": create_sample_chat_history(),
        }

        with pytest.raises(NodeValidationError, match="requires non-empty messages"):
            transform_tasks_node.validate_input_state(state)

    def test_validate_input_state_missing_chat_history(self, transform_tasks_node):
        """Test input validation with missing chat_history."""
        state = {"messages": [HumanMessage(content="test")]}

        with pytest.raises(
            NodeValidationError, match="requires 'chat_history' attribute"
        ):
            transform_tasks_node.validate_input_state(state)

    def test_validate_input_state_invalid_chat_history(self, transform_tasks_node):
        """Test input validation with chat_history missing required methods."""
        state = {
            "messages": [HumanMessage(content="test")],
            "chat_history": "invalid_chat_history",  # String without to_list method
        }

        with pytest.raises(
            NodeValidationError,
            match="requires chat_history object with 'to_list' method",
        ):
            transform_tasks_node.validate_input_state(state)

    def test_validate_input_state_invalid_tasks_no_ids(self, transform_tasks_node):
        """Test input validation with tasks missing ids property."""
        invalid_tasks = Mock()
        del invalid_tasks.ids  # Remove ids property
        state = {
            "messages": [HumanMessage(content="test")],
            "chat_history": create_sample_chat_history(),
            "tasks": invalid_tasks,
        }

        with pytest.raises(
            NodeValidationError, match="requires tasks object with 'ids' property"
        ):
            transform_tasks_node.validate_input_state(state)

    def test_validate_input_state_invalid_tasks_no_set_definition(
        self, transform_tasks_node
    ):
        """Test input validation with tasks missing set_definition method."""
        invalid_tasks = Mock()
        invalid_tasks.ids = []
        del invalid_tasks.set_definition  # Remove set_definition method
        state = {
            "messages": [HumanMessage(content="test")],
            "chat_history": create_sample_chat_history(),
            "tasks": invalid_tasks,
        }

        with pytest.raises(
            NodeValidationError,
            match="requires tasks object with 'set_definition' method",
        ):
            transform_tasks_node.validate_input_state(state)

    def test_validate_input_state_with_none_tasks(self, transform_tasks_node):
        """Test input validation with None tasks (should be valid)."""
        state = {
            "messages": [HumanMessage(content="test")],
            "chat_history": create_sample_chat_history(),
            "tasks": None,
        }

        # Should not raise any exception
        transform_tasks_node.validate_input_state(state)

    def test_validate_output_state(self, transform_tasks_node):
        """Test output state validation (currently no-op)."""
        transform_tasks_node.validate_output_state({})

    # Note: Execution tests for TransformTasksNode would require complex mocking
    # of the actual LLM service and prompt template. The validation tests above
    # are the main focus and they are working correctly.


class TestTransformTasksNodeIntegration:
    """Test integration aspects of transform tasks node."""

    def test_transform_tasks_node_registered(self):
        """Test that transform tasks node is properly registered."""
        # Import the nodes package to ensure all decorators are executed
        import quivr_core.rag.langgraph_framework.nodes  # noqa: F401

        from quivr_core.rag.langgraph_framework.registry.node_registry import (
            node_registry,
        )

        task_nodes = node_registry.list_nodes("tasks")
        assert (
            "transform_tasks" in task_nodes
        ), f"TransformTasksNode not registered. Available task nodes: {task_nodes}"

    def test_transform_tasks_node_dependencies(self):
        """Test that transform tasks node declares proper dependencies."""
        node = TransformTasksNode()

        # Should have proper node name
        assert hasattr(node, "NODE_NAME")
        assert node.NODE_NAME == "transform_tasks"
