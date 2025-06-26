"""Tests for tool nodes."""

import pytest
from unittest.mock import Mock, AsyncMock, patch

from quivr_core.rag.langgraph_framework.nodes.tools.run_tool_node import RunToolNode
from quivr_core.rag.langgraph_framework.base.exceptions import NodeValidationError

from tests.rag.langgraph_framework.fixtures.test_data import (
    create_sample_agent_state,
    create_sample_user_tasks,
)


class TestRunToolNode:
    """Test RunToolNode functionality."""

    @pytest.fixture(scope="function")
    def run_tool_node(self):
        """Create a RunToolNode instance."""
        return RunToolNode()

    @pytest.fixture(scope="function")
    def valid_state_with_tools(self):
        """Create a valid state with tool information."""
        state = create_sample_agent_state()
        tasks = create_sample_user_tasks()

        # Set up tasks with supported tools
        if tasks.ids:
            task_id = tasks.ids[0]
            tasks.set_tool(task_id, "tavily")  # Use supported tool
            tasks.set_completion(task_id, False)  # Non-completable task

        state["tasks"] = tasks
        return state

    def test_node_name(self, run_tool_node):
        """Test node name."""
        assert run_tool_node.NODE_NAME == "run_tool"

    def test_validate_input_state_success(self, run_tool_node, valid_state_with_tools):
        """Test successful input state validation."""
        run_tool_node.validate_input_state(valid_state_with_tools)

    def test_validate_input_state_missing_tasks(self, run_tool_node):
        """Test input validation with missing tasks."""
        state = {"messages": []}

        with pytest.raises(NodeValidationError, match="requires 'tasks' attribute"):
            run_tool_node.validate_input_state(state)

    def test_validate_input_state_empty_tasks(self, run_tool_node):
        """Test input validation with empty tasks."""
        state = {"tasks": None}

        with pytest.raises(NodeValidationError, match="requires non-empty tasks"):
            run_tool_node.validate_input_state(state)

    def test_validate_input_state_invalid_tasks_no_has_tasks(self, run_tool_node):
        """Test input validation with tasks missing has_tasks method."""
        invalid_tasks = Mock(spec=[])  # Mock without has_tasks method
        state = {"tasks": invalid_tasks}

        with pytest.raises(
            NodeValidationError, match="requires tasks object with 'has_tasks' method"
        ):
            run_tool_node.validate_input_state(state)

    def test_validate_input_state_invalid_tasks_no_ids(self, run_tool_node):
        """Test input validation with tasks missing ids property."""
        invalid_tasks = Mock()
        invalid_tasks.has_tasks = Mock()
        del invalid_tasks.ids  # Remove ids property
        state = {"tasks": invalid_tasks}

        with pytest.raises(
            NodeValidationError, match="requires tasks object with 'ids' property"
        ):
            run_tool_node.validate_input_state(state)

    def test_validate_input_state_invalid_tasks_no_set_docs(self, run_tool_node):
        """Test input validation with tasks missing set_docs method."""
        invalid_tasks = Mock()
        invalid_tasks.has_tasks = Mock()
        invalid_tasks.ids = []
        del invalid_tasks.set_docs  # Remove set_docs method
        state = {"tasks": invalid_tasks}

        with pytest.raises(
            NodeValidationError, match="requires tasks object with 'set_docs' method"
        ):
            run_tool_node.validate_input_state(state)

    def test_validate_output_state(self, run_tool_node):
        """Test output state validation (currently no-op)."""
        run_tool_node.validate_output_state({})

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_with_tool_execution(
        self, run_tool_node, valid_state_with_tools
    ):
        """Test successful tool execution."""
        # Mock the LLMToolFactory to avoid actual tool creation
        with patch(
            "quivr_core.rag.langgraph_framework.nodes.tools.run_tool_node.LLMToolFactory"
        ) as mock_factory:
            # Mock tool wrapper
            mock_tool = Mock()
            mock_tool.ainvoke = AsyncMock(
                return_value="Search results: Found 5 relevant documents"
            )

            mock_wrapper = Mock()
            mock_wrapper.tool = mock_tool
            mock_wrapper.format_input.return_value = "formatted_input"
            mock_wrapper.format_output.return_value = [Mock()]  # Mock documents

            mock_factory.create_tool.return_value = mock_wrapper

            result = await run_tool_node.execute(valid_state_with_tools)

        # Should return state with updated tasks
        assert "tasks" in result

        # Should have called create_tool with correct parameters
        mock_factory.create_tool.assert_called_once_with("tavily", {})

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_multiple_tools(self, run_tool_node):
        """Test execution with multiple tools for different tasks."""
        state = create_sample_agent_state()
        tasks = create_sample_user_tasks()

        # Set up multiple tasks with different supported tools
        if len(tasks.ids) >= 2:
            tasks.set_tool(tasks.ids[0], "tavily")
            tasks.set_completion(tasks.ids[0], False)
            tasks.set_tool(tasks.ids[1], "cited_answer")
            tasks.set_completion(tasks.ids[1], False)

        state["tasks"] = tasks

        # Mock the LLMToolFactory
        with patch(
            "quivr_core.rag.langgraph_framework.nodes.tools.run_tool_node.LLMToolFactory"
        ) as mock_factory:
            # Mock different tool wrappers
            def mock_create_tool(tool_name, config):
                mock_tool = Mock()
                mock_tool.ainvoke = AsyncMock(return_value=f"{tool_name} result")

                mock_wrapper = Mock()
                mock_wrapper.tool = mock_tool
                mock_wrapper.format_input.return_value = "formatted_input"
                mock_wrapper.format_output.return_value = [Mock()]

                return mock_wrapper

            mock_factory.create_tool.side_effect = mock_create_tool

            result = await run_tool_node.execute(state)

        # Should have processed multiple tools
        assert "tasks" in result
        assert mock_factory.create_tool.call_count == 2

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_with_no_tools_needed(self, run_tool_node):
        """Test execution when no tools are needed."""
        state = create_sample_agent_state()
        tasks = create_sample_user_tasks()

        # Set all tasks as completable (no tools needed)
        for task_id in tasks.ids:
            tasks.set_completion(task_id, True)

        state["tasks"] = tasks

        result = await run_tool_node.execute(state)

        # Should return the state with tasks
        assert "tasks" in result
        assert result["tasks"] == tasks

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_with_tool_error(self, run_tool_node, valid_state_with_tools):
        """Test handling of tool execution errors."""
        # Mock the LLMToolFactory to raise an error
        with patch(
            "quivr_core.rag.langgraph_framework.nodes.tools.run_tool_node.LLMToolFactory"
        ) as mock_factory:
            mock_factory.create_tool.side_effect = ValueError(
                "Tool tavily is not supported."
            )

            # Should propagate the error
            with pytest.raises(ValueError, match="Tool tavily is not supported."):
                await run_tool_node.execute(valid_state_with_tools)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_with_custom_config(
        self, run_tool_node, valid_state_with_tools
    ):
        """Test execution with custom configuration."""
        custom_config = Mock()

        # Mock the LLMToolFactory
        with patch(
            "quivr_core.rag.langgraph_framework.nodes.tools.run_tool_node.LLMToolFactory"
        ) as mock_factory:
            mock_tool = Mock()
            mock_tool.ainvoke = AsyncMock(return_value="Tool result")

            mock_wrapper = Mock()
            mock_wrapper.tool = mock_tool
            mock_wrapper.format_input.return_value = "formatted_input"
            mock_wrapper.format_output.return_value = [Mock()]

            mock_factory.create_tool.return_value = mock_wrapper

            result = await run_tool_node.execute(valid_state_with_tools, custom_config)

        # Should have executed successfully
        assert "tasks" in result

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_task_completion_after_tools(
        self, run_tool_node, valid_state_with_tools
    ):
        """Test that tasks are updated after tool execution."""
        # Mock the LLMToolFactory
        with patch(
            "quivr_core.rag.langgraph_framework.nodes.tools.run_tool_node.LLMToolFactory"
        ) as mock_factory:
            mock_tool = Mock()
            mock_tool.ainvoke = AsyncMock(return_value="Tool completed successfully")

            mock_wrapper = Mock()
            mock_wrapper.tool = mock_tool
            mock_wrapper.format_input.return_value = "formatted_input"
            mock_wrapper.format_output.return_value = [Mock()]  # Mock documents

            mock_factory.create_tool.return_value = mock_wrapper

            result = await run_tool_node.execute(valid_state_with_tools)

        # Check that tasks state is updated
        assert "tasks" in result
        tasks = result["tasks"]

        # Tasks should have been processed
        assert tasks is not None


class TestRunToolNodeIntegration:
    """Test integration aspects of run tool node."""

    def test_run_tool_node_registered(self):
        """Test that run tool node is properly registered."""
        # Import the nodes package to ensure all decorators are executed
        import quivr_core.rag.langgraph_framework.nodes  # noqa: F401

        from quivr_core.rag.langgraph_framework.registry.node_registry import (
            node_registry,
        )

        tool_nodes = node_registry.list_nodes("tools")
        assert (
            "run_tool" in tool_nodes
        ), f"RunToolNode not registered. Available tool nodes: {tool_nodes}"

    def test_run_tool_node_dependencies(self):
        """Test that run tool node declares proper dependencies."""
        node = RunToolNode()

        # Should have proper node name
        assert hasattr(node, "NODE_NAME")
        assert node.NODE_NAME == "run_tool"

    @pytest.mark.asyncio(loop_scope="session")
    async def test_run_tool_node_with_real_task_structure(self):
        """Test run tool node with realistic task structure."""
        from quivr_core.rag.langgraph_framework.task import UserTasks

        # Create realistic task structure
        tasks = UserTasks(["Search for recent AI papers", "Generate a cited answer"])

        # Set up tasks with supported tools
        if len(tasks.ids) >= 2:
            tasks.set_tool(tasks.ids[0], "tavily")
            tasks.set_completion(tasks.ids[0], False)
            tasks.set_tool(tasks.ids[1], "cited_answer")
            tasks.set_completion(tasks.ids[1], False)

        state = create_sample_agent_state()
        state["tasks"] = tasks

        node = RunToolNode()

        # Mock the LLMToolFactory
        with patch(
            "quivr_core.rag.langgraph_framework.nodes.tools.run_tool_node.LLMToolFactory"
        ) as mock_factory:
            # Mock realistic tool responses
            def mock_create_tool(tool_name, config):
                mock_tool = Mock()
                if tool_name == "tavily":
                    mock_tool.ainvoke = AsyncMock(
                        return_value="Found 10 recent AI papers on arxiv.org"
                    )
                elif tool_name == "cited_answer":
                    mock_tool.ainvoke = AsyncMock(return_value="Generated cited answer")
                else:
                    mock_tool.ainvoke = AsyncMock(return_value="Tool executed")

                mock_wrapper = Mock()
                mock_wrapper.tool = mock_tool
                mock_wrapper.format_input.return_value = "formatted_input"
                mock_wrapper.format_output.return_value = [Mock()]

                return mock_wrapper

            mock_factory.create_tool.side_effect = mock_create_tool

            result = await node.execute(state)

        # Should have processed the tasks
        assert result is not None
        assert "tasks" in result
        assert "messages" in result
