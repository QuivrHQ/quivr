"""Tests for routing nodes."""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from langgraph.types import Send

from quivr_core.rag.entities.config import (
    LLMEndpointConfig,
    WorkflowConfig,
)
from quivr_core.rag.entities.prompt import PromptConfig
from quivr_core.rag.langgraph_framework.nodes.routing.routing_node import RoutingNode
from quivr_core.rag.langgraph_framework.nodes.routing.tool_routing_node import (
    ToolRoutingNode,
)
from quivr_core.rag.langgraph_framework.base.exceptions import NodeValidationError
from quivr_core.rag.langgraph_framework.entities.routing_entity import (
    SplittedInputWithInstructions,
)
from quivr_core.rag.langgraph_framework.state import TasksCompletion
from quivr_core.rag.langgraph_framework.task import UserTasks

from tests.rag.langgraph_framework.fixtures.test_data import (
    create_sample_agent_state,
    create_sample_user_tasks,
)


class TestRoutingNode:
    """Test basic RoutingNode functionality."""

    @pytest.fixture(scope="function")
    def routing_node(self):
        """Create a RoutingNode instance."""
        return RoutingNode()

    @pytest.fixture(scope="function")
    def valid_state(self):
        """Create a valid state for testing."""
        state = create_sample_agent_state()
        state["tasks"] = create_sample_user_tasks()
        return state

    def test_node_name(self, routing_node):
        """Test node name and configuration types."""
        assert routing_node.NODE_NAME == "routing"

    def test_validate_input_state_success(self, routing_node, valid_state):
        """Test successful input state validation."""
        routing_node.validate_input_state(valid_state)

    def test_validate_input_state_missing_messages(self, routing_node):
        """Test input validation with missing messages."""
        state = {"tasks": create_sample_user_tasks()}

        with pytest.raises(NodeValidationError, match="requires 'messages' attribute"):
            routing_node.validate_input_state(state)

    def test_validate_input_state_empty_messages(self, routing_node):
        """Test input validation with empty messages."""
        state = {"messages": [], "tasks": create_sample_user_tasks()}

        with pytest.raises(NodeValidationError, match="requires non-empty messages"):
            routing_node.validate_input_state(state)

    def test_validate_input_state_missing_chat_history(self, routing_node):
        """Test input validation with missing chat_history."""
        from langchain_core.messages import HumanMessage

        state = {"messages": [HumanMessage(content="test")]}

        with pytest.raises(
            NodeValidationError, match="requires 'chat_history' attribute"
        ):
            routing_node.validate_input_state(state)

    def test_validate_output_state(self, routing_node):
        """Test output state validation (currently no-op)."""
        routing_node.validate_output_state({})

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_with_instructions(self, routing_node, valid_state):
        """Test execution when LLM returns instructions."""
        mock_llm_service = Mock()

        # Mock LLM response with instructions
        mock_response = SplittedInputWithInstructions(
            instructions="Custom instructions for the task", task_list=None
        )
        mock_llm_service.invoke_with_structured_output = AsyncMock(
            return_value=mock_response
        )

        with patch("quivr_core.rag.prompt.registry.get_prompt") as mock_get_prompt:
            # Mock prompt template
            mock_template = Mock()
            mock_template.format.return_value = "Formatted routing prompt"
            mock_get_prompt.return_value = mock_template

            with patch.object(
                routing_node, "get_service", return_value=mock_llm_service
            ):
                result = await routing_node.execute(valid_state)

        # Should return Send for edit_system_prompt
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Send)
        assert result[0].node == "edit_system_prompt"
        assert result[0].arg["instructions"] == "Custom instructions for the task"

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_with_task_list(self, routing_node, valid_state):
        """Test execution when LLM returns task list."""
        mock_llm_service = Mock()

        # Mock LLM response with task list
        mock_response = SplittedInputWithInstructions(
            instructions=None, task_list=["Task 1", "Task 2", "Task 3"]
        )
        mock_llm_service.invoke_with_structured_output = AsyncMock(
            return_value=mock_response
        )

        with patch("quivr_core.rag.prompt.registry.get_prompt") as mock_get_prompt:
            # Mock prompt template
            mock_template = Mock()
            mock_template.format.return_value = "Formatted routing prompt"
            mock_get_prompt.return_value = mock_template

            with patch.object(
                routing_node, "get_service", return_value=mock_llm_service
            ):
                result = await routing_node.execute(valid_state)

        # Should return Send for filter_history
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Send)
        assert result[0].node == "filter_history"
        assert "chat_history" in result[0].arg
        assert "tasks" in result[0].arg

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_with_prompt_config_fallback(self, routing_node, valid_state):
        """Test execution with prompt config fallback when no instructions."""
        mock_llm_service = Mock()

        # Mock LLM response with no instructions
        mock_response = SplittedInputWithInstructions(instructions=None, task_list=None)
        mock_llm_service.invoke_with_structured_output = AsyncMock(
            return_value=mock_response
        )

        # Mock prompt config with fallback prompt
        mock_prompt_config = PromptConfig(prompt="Fallback prompt instructions")

        with patch("quivr_core.rag.prompt.registry.get_prompt") as mock_get_prompt:
            # Mock prompt template
            mock_template = Mock()
            mock_template.format.return_value = "Formatted routing prompt"
            mock_get_prompt.return_value = mock_template

            with patch.object(
                routing_node, "get_service", return_value=mock_llm_service
            ):
                with patch.object(
                    routing_node, "get_config", return_value=mock_prompt_config
                ):
                    result = await routing_node.execute(valid_state)

        # Should return Send for edit_system_prompt with fallback prompt
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Send)
        assert result[0].node == "edit_system_prompt"
        assert result[0].arg["instructions"] == "Fallback prompt instructions"


class TestToolRoutingNode:
    """Test ToolRoutingNode functionality."""

    @pytest.fixture(scope="function")
    def tool_routing_node(self):
        """Create a ToolRoutingNode instance."""
        return ToolRoutingNode()

    @pytest.fixture(scope="function")
    def valid_state_with_tasks(self):
        """Create a valid state with tasks for testing."""
        state = create_sample_agent_state()
        tasks = create_sample_user_tasks()
        state["tasks"] = tasks
        return state

    def test_node_name(self, tool_routing_node):
        """Test node name and configuration types."""
        assert tool_routing_node.NODE_NAME == "tool_routing"

    def test_validate_input_state_success(
        self, tool_routing_node, valid_state_with_tasks
    ):
        """Test successful input state validation."""
        tool_routing_node.validate_input_state(valid_state_with_tasks)

    def test_validate_input_state_missing_tasks(self, tool_routing_node):
        """Test input validation with missing tasks."""
        state = {"chat_history": Mock()}

        with pytest.raises(NodeValidationError, match="requires 'tasks' attribute"):
            tool_routing_node.validate_input_state(state)

    def test_validate_input_state_empty_tasks(self, tool_routing_node):
        """Test input validation with empty tasks."""
        state = {"tasks": None, "chat_history": Mock()}

        with pytest.raises(NodeValidationError, match="requires non-empty tasks"):
            tool_routing_node.validate_input_state(state)

    def test_validate_input_state_invalid_tasks_no_has_tasks(self, tool_routing_node):
        """Test input validation with tasks missing has_tasks method."""
        invalid_tasks = Mock(spec=[])  # Mock without has_tasks method
        state = {"tasks": invalid_tasks, "chat_history": Mock()}

        with pytest.raises(
            NodeValidationError, match="requires tasks object with 'has_tasks' method"
        ):
            tool_routing_node.validate_input_state(state)

    def test_validate_input_state_invalid_tasks_no_ids(self, tool_routing_node):
        """Test input validation with tasks missing ids property."""
        invalid_tasks = Mock()
        invalid_tasks.has_tasks = Mock()
        del invalid_tasks.ids  # Remove ids property
        state = {"tasks": invalid_tasks, "chat_history": Mock()}

        with pytest.raises(
            NodeValidationError, match="requires tasks object with 'ids' property"
        ):
            tool_routing_node.validate_input_state(state)

    def test_validate_input_state_missing_chat_history(self, tool_routing_node):
        """Test input validation with missing chat_history."""
        valid_tasks = Mock()
        valid_tasks.has_tasks = Mock()
        valid_tasks.ids = []
        state = {"tasks": valid_tasks}

        with pytest.raises(
            NodeValidationError, match="requires 'chat_history' attribute"
        ):
            tool_routing_node.validate_input_state(state)

    def test_validate_input_state_invalid_chat_history(self, tool_routing_node):
        """Test input validation with chat_history missing required methods."""
        valid_tasks = Mock()
        valid_tasks.has_tasks = Mock()
        valid_tasks.ids = []
        state = {
            "tasks": valid_tasks,
            "chat_history": "invalid_chat_history",  # String without to_list method
        }

        with pytest.raises(
            NodeValidationError,
            match="requires chat_history object with 'to_list' method",
        ):
            tool_routing_node.validate_input_state(state)

    def test_validate_output_state(self, tool_routing_node):
        """Test output state validation (currently no-op)."""
        tool_routing_node.validate_output_state({})

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_no_tasks(self, tool_routing_node):
        """Test execution when there are no tasks."""
        state = create_sample_agent_state()
        empty_tasks = UserTasks([])  # Empty task list
        state["tasks"] = empty_tasks

        with patch.object(tool_routing_node, "get_config") as mock_get_config:
            mock_get_config.side_effect = [
                LLMEndpointConfig(),
                WorkflowConfig(),
            ]

            result = await tool_routing_node.execute(state)

        # Should route directly to generate_rag when no tasks
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Send)
        assert result[0].node == "generate_rag"

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_with_completable_tasks(
        self, tool_routing_node, valid_state_with_tasks
    ):
        """Test execution with completable tasks."""
        mock_llm_service = Mock()
        mock_prompt_service = Mock()

        # Mock LLM responses indicating tasks are completable
        mock_response = TasksCompletion(is_task_completable=True, tool=None)
        mock_llm_service.invoke_with_structured_output = AsyncMock(
            return_value=mock_response
        )

        # Mock prompt service
        mock_template = Mock()
        mock_template.format.return_value = "Formatted tool routing prompt"
        mock_prompt_service.get_template.return_value = mock_template

        with patch.object(tool_routing_node, "get_service") as mock_get_service:
            mock_get_service.side_effect = [mock_llm_service, mock_prompt_service]

            with patch.object(tool_routing_node, "get_config") as mock_get_config:
                mock_get_config.side_effect = [
                    PromptConfig(),
                    LLMEndpointConfig(),
                    WorkflowConfig(),
                ]

                # Mock collect_tools
                with patch(
                    "quivr_core.rag.langgraph_framework.nodes.routing.tool_routing_node.collect_tools"
                ) as mock_collect:
                    mock_collect.return_value = ("validated_tools", "activated_tools")

                    # Mock combine_documents
                    with patch(
                        "quivr_core.rag.langgraph_framework.nodes.routing.tool_routing_node.combine_documents"
                    ) as mock_combine:
                        mock_combine.return_value = "combined_docs"

                        result = await tool_routing_node.execute(valid_state_with_tasks)

        # Should route to generate_rag when all tasks are completable
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Send)
        assert result[0].node == "generate_rag"

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_with_non_completable_tasks(
        self, tool_routing_node, valid_state_with_tasks
    ):
        """Test execution with non-completable tasks requiring tools."""
        mock_llm_service = Mock()
        mock_prompt_service = Mock()

        # Mock LLM responses indicating tasks need tools
        mock_response = TasksCompletion(is_task_completable=False, tool="search_tool")
        mock_llm_service.invoke_with_structured_output = AsyncMock(
            return_value=mock_response
        )

        # Mock prompt service
        mock_template = Mock()
        mock_template.format.return_value = "Formatted tool routing prompt"
        mock_prompt_service.get_template.return_value = mock_template

        with patch.object(tool_routing_node, "get_service") as mock_get_service:
            mock_get_service.side_effect = [mock_llm_service, mock_prompt_service]

            with patch.object(tool_routing_node, "get_config") as mock_get_config:
                mock_get_config.side_effect = [
                    PromptConfig(),
                    LLMEndpointConfig(),
                    WorkflowConfig(),
                ]

                # Mock collect_tools
                with patch(
                    "quivr_core.rag.langgraph_framework.nodes.routing.tool_routing_node.collect_tools"
                ) as mock_collect:
                    mock_collect.return_value = ("validated_tools", "activated_tools")

                    # Mock combine_documents
                    with patch(
                        "quivr_core.rag.langgraph_framework.nodes.routing.tool_routing_node.combine_documents"
                    ) as mock_combine:
                        mock_combine.return_value = "combined_docs"

                        result = await tool_routing_node.execute(valid_state_with_tasks)

        # Should route to run_tool when tasks are not completable
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Send)
        assert result[0].node == "run_tool"

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_multiple_tasks_mixed_completion(self, tool_routing_node):
        """Test execution with multiple tasks having mixed completion status."""
        state = create_sample_agent_state()
        tasks = UserTasks(["Task 1", "Task 2", "Task 3"])
        state["tasks"] = tasks

        mock_llm_service = Mock()
        mock_prompt_service = Mock()

        # Mock different responses for different tasks
        responses = [
            TasksCompletion(is_task_completable=True, tool=None),
            TasksCompletion(is_task_completable=False, tool="search_tool"),
            TasksCompletion(is_task_completable=False, tool="calculator_tool"),
        ]
        mock_llm_service.invoke_with_structured_output = AsyncMock(
            side_effect=responses
        )

        # Mock prompt service
        mock_template = Mock()
        mock_template.format.return_value = "Formatted tool routing prompt"
        mock_prompt_service.get_template.return_value = mock_template

        with patch.object(tool_routing_node, "get_service") as mock_get_service:
            mock_get_service.side_effect = [mock_llm_service, mock_prompt_service]

            with patch.object(tool_routing_node, "get_config") as mock_get_config:
                mock_get_config.side_effect = [
                    PromptConfig(),
                    LLMEndpointConfig(),
                    WorkflowConfig(),
                ]

                # Mock collect_tools
                with patch(
                    "quivr_core.rag.langgraph_framework.nodes.routing.tool_routing_node.collect_tools"
                ) as mock_collect:
                    mock_collect.return_value = ("validated_tools", "activated_tools")

                    # Mock combine_documents
                    with patch(
                        "quivr_core.rag.langgraph_framework.nodes.routing.tool_routing_node.combine_documents"
                    ) as mock_combine:
                        mock_combine.return_value = "combined_docs"

                        result = await tool_routing_node.execute(state)

        # Should route to run_tool because some tasks are not completable
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], Send)
        assert result[0].node == "run_tool"

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_async_processing(self, tool_routing_node):
        """Test that multiple tasks are processed asynchronously."""
        state = create_sample_agent_state()
        tasks = UserTasks(["Task 1", "Task 2"])
        state["tasks"] = tasks

        mock_llm_service = Mock()
        mock_prompt_service = Mock()

        # Mock async responses - return actual coroutines
        mock_responses = [
            TasksCompletion(is_task_completable=True, tool=None),
            TasksCompletion(is_task_completable=True, tool=None),
        ]

        mock_llm_service.invoke_with_structured_output = AsyncMock(
            side_effect=mock_responses
        )

        # Mock prompt service
        mock_template = Mock()
        mock_template.format.return_value = "Formatted tool routing prompt"
        mock_prompt_service.get_template.return_value = mock_template

        with patch.object(tool_routing_node, "get_service") as mock_get_service:
            mock_get_service.side_effect = [mock_llm_service, mock_prompt_service]

            with patch.object(tool_routing_node, "get_config") as mock_get_config:
                mock_get_config.side_effect = [
                    PromptConfig(),
                    LLMEndpointConfig(),
                    WorkflowConfig(),
                ]

                # Mock collect_tools and combine_documents
                with patch(
                    "quivr_core.rag.langgraph_framework.nodes.routing.tool_routing_node.collect_tools"
                ) as mock_collect:
                    mock_collect.return_value = ("validated_tools", "activated_tools")

                    with patch(
                        "quivr_core.rag.langgraph_framework.nodes.routing.tool_routing_node.combine_documents"
                    ) as mock_combine:
                        mock_combine.return_value = "combined_docs"

                        result = await tool_routing_node.execute(state)

                        # Verify the LLM service was called for each task
                        assert (
                            mock_llm_service.invoke_with_structured_output.call_count
                            == 2
                        )

                        # Should route to generate_rag when all tasks are completable
                        assert isinstance(result, list)
                        assert len(result) == 1
                        assert isinstance(result[0], Send)
                        assert result[0].node == "generate_rag"


class TestRoutingNodeErrorHandling:
    """Test error handling across routing nodes."""

    @pytest.fixture(scope="function")
    def routing_node(self):
        """Create a RoutingNode instance."""
        return RoutingNode()

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_with_llm_error(self, routing_node):
        """Test handling of LLM errors during routing."""
        state = create_sample_agent_state()

        mock_llm_service = Mock()

        # Mock LLM error
        mock_llm_service.invoke_with_structured_output = AsyncMock(
            side_effect=Exception("LLM service unavailable")
        )

        with patch("quivr_core.rag.prompt.registry.get_prompt") as mock_get_prompt:
            # Mock prompt template
            mock_template = Mock()
            mock_template.format.return_value = "Formatted prompt"
            mock_get_prompt.return_value = mock_template

            with patch.object(
                routing_node, "get_service", return_value=mock_llm_service
            ):
                with pytest.raises(Exception, match="LLM service unavailable"):
                    await routing_node.execute(state)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_with_config_error(self, routing_node):
        """Test handling of configuration errors."""
        state = create_sample_agent_state()

        with patch.object(routing_node, "get_config") as mock_get_config:
            mock_get_config.side_effect = Exception("Invalid configuration")

            with pytest.raises(Exception, match="Invalid configuration"):
                await routing_node.execute(state)


class TestRoutingNodeIntegration:
    """Test integration aspects of routing nodes."""

    def test_all_routing_nodes_registered(self):
        """Test that all routing nodes are properly registered."""
        # Import the nodes package to ensure all decorators are executed
        import quivr_core.rag.langgraph_framework.nodes  # noqa: F401

        from quivr_core.rag.langgraph_framework.registry.node_registry import (
            node_registry,
        )

        routing_nodes = node_registry.list_nodes("routing")

        expected_nodes = ["routing", "routing_split", "tool_routing"]

        for expected_node in expected_nodes:
            assert (
                expected_node in routing_nodes
            ), f"Node {expected_node} not registered. Available routing nodes: {routing_nodes}"

    def test_routing_nodes_have_proper_dependencies(self):
        """Test that routing nodes declare proper dependencies."""
        nodes = [
            RoutingNode(),
            ToolRoutingNode(),
        ]

        for node in nodes:
            # All routing nodes should have proper node names
            assert hasattr(node, "NODE_NAME")
            assert node.NODE_NAME is not None

    def test_routing_node_send_structure(self):
        """Test that routing nodes return proper Send structures."""
        # This is a structural test to ensure Send objects are properly formed
        from langgraph.types import Send

        # Test Send creation
        send_obj = Send("test_node", {"test": "data"})
        assert send_obj.node == "test_node"
        assert send_obj.arg == {"test": "data"}
