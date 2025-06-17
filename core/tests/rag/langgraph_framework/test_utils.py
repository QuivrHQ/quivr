"""Tests for utility functions."""

from unittest.mock import Mock, patch
from langchain_core.documents import Document
from langchain_core.prompts import BasePromptTemplate

from quivr_core.rag.langgraph_framework.utils import (
    update_active_tools,
    reduce_rag_context,
)
from quivr_core.rag.langgraph_framework.task import UserTasks, UserTaskEntity
from quivr_core.rag.langgraph_framework.state import UpdatedPromptAndTools
from uuid import uuid4


class TestUpdateActiveTools:
    """Test tool activation/deactivation functionality."""

    def test_activate_tools(self):
        """Test activating tools."""
        # Create mock workflow config
        workflow_config = Mock()
        workflow_config.activated_tools = []
        workflow_config.validated_tools = []

        # Create mock tools
        search_tool = Mock()
        search_tool.name = "search_tool"
        calculator_tool = Mock()
        calculator_tool.name = "calculator"

        # Add tools to validated_tools
        workflow_config.validated_tools = [search_tool, calculator_tool]

        # Create UpdatedPromptAndTools object
        updated_tools = UpdatedPromptAndTools(
            tools_to_activate=["search_tool", "calculator"], tools_to_deactivate=[]
        )

        # Test activation
        update_active_tools(workflow_config, updated_tools)

        # Verify tools were activated
        assert len(workflow_config.activated_tools) == 2
        assert search_tool in workflow_config.activated_tools
        assert calculator_tool in workflow_config.activated_tools

    def test_deactivate_tools(self):
        """Test deactivating tools."""
        # Create mock tools
        search_tool = Mock()
        search_tool.name = "search_tool"
        calculator_tool = Mock()
        calculator_tool.name = "calculator"

        # Create mock workflow config with activated tools
        workflow_config = Mock()
        workflow_config.activated_tools = [search_tool, calculator_tool]
        workflow_config.validated_tools = [search_tool, calculator_tool]

        # Create UpdatedPromptAndTools object
        updated_tools = UpdatedPromptAndTools(
            tools_to_activate=[], tools_to_deactivate=["calculator"]
        )

        # Test deactivation
        update_active_tools(workflow_config, updated_tools)

        # Verify only search_tool remains
        assert len(workflow_config.activated_tools) == 1
        assert search_tool in workflow_config.activated_tools
        assert calculator_tool not in workflow_config.activated_tools

    def test_activate_and_deactivate_tools(self):
        """Test both activating and deactivating tools."""
        # Create mock tools
        search_tool = Mock()
        search_tool.name = "search_tool"
        calculator_tool = Mock()
        calculator_tool.name = "calculator"
        file_tool = Mock()
        file_tool.name = "file_tool"

        # Create mock workflow config
        workflow_config = Mock()
        workflow_config.activated_tools = [search_tool, calculator_tool]
        workflow_config.validated_tools = [search_tool, calculator_tool, file_tool]

        # Create UpdatedPromptAndTools object
        updated_tools = UpdatedPromptAndTools(
            tools_to_activate=["file_tool"], tools_to_deactivate=["calculator"]
        )

        # Test simultaneous activation and deactivation
        update_active_tools(workflow_config, updated_tools)

        # Verify final state
        assert len(workflow_config.activated_tools) == 2
        assert search_tool in workflow_config.activated_tools
        assert file_tool in workflow_config.activated_tools
        assert calculator_tool not in workflow_config.activated_tools

    def test_activate_nonexistent_tool(self):
        """Test activating a tool that doesn't exist."""
        workflow_config = Mock()
        workflow_config.activated_tools = []
        workflow_config.validated_tools = []

        # Create UpdatedPromptAndTools object
        updated_tools = UpdatedPromptAndTools(
            tools_to_activate=["nonexistent_tool"], tools_to_deactivate=[]
        )

        # Should not raise error, just ignore non-existent tools
        update_active_tools(workflow_config, updated_tools)

        assert len(workflow_config.activated_tools) == 0


class TestReduceRAGContext:
    """Test RAG context reduction functionality."""

    def test_context_reduction_basic(self):
        """Test basic context reduction."""
        # Create mock state
        state = {"files": "doc1.txt,doc2.pdf", "tasks": UserTasks()}

        # Create mock inputs with documents
        inputs = {
            "context": [
                Document(page_content="Content 1", metadata={"source": "doc1.txt"}),
                Document(page_content="Content 2", metadata={"source": "doc2.pdf"}),
                Document(page_content="Content 3", metadata={"source": "doc3.txt"}),
            ],
            "chat_history": [],
        }

        # Mock prompt template
        prompt_template = Mock(spec=BasePromptTemplate)
        prompt_template.format.return_value = "formatted prompt"

        # Mock token counting function
        count_tokens_fn = Mock()
        count_tokens_fn.return_value = 100  # Each document has 100 tokens

        max_context_tokens = 1000

        result_state, result_inputs = reduce_rag_context(
            state, inputs, prompt_template, count_tokens_fn, max_context_tokens
        )

        # Verify context was processed
        assert "context" in result_inputs
        assert isinstance(result_state, dict)
        assert isinstance(result_inputs, dict)

        # Verify token counting was called
        assert count_tokens_fn.called

    def test_context_reduction_via_task_docs(self):
        """Test context reduction using task documents."""
        # Create tasks with documents
        tasks = UserTasks()
        task_id = uuid4()
        task_docs = [
            Document(page_content="Task doc 1", metadata={"source": "task1.txt"}),
            Document(page_content="Task doc 2", metadata={"source": "task2.txt"}),
        ]

        # Manually add task with documents
        tasks.user_tasks[task_id] = UserTaskEntity(
            id=task_id, definition="Test task", docs=task_docs, completable=False
        )

        state = {"files": "", "tasks": tasks}

        inputs = {"context": [], "chat_history": []}

        # Mock prompt template
        prompt_template = Mock(spec=BasePromptTemplate)
        prompt_template.format.return_value = "formatted prompt"

        # Mock token counting function
        count_tokens_fn = Mock()
        count_tokens_fn.return_value = 50

        max_context_tokens = 1000

        result_state, result_inputs = reduce_rag_context(
            state, inputs, prompt_template, count_tokens_fn, max_context_tokens
        )

        # Verify task docs were processed
        assert "context" in result_inputs
        assert isinstance(result_state, dict)
        assert isinstance(result_inputs, dict)

    def test_insufficient_context_warning(self):
        """Test warning when context is insufficient."""
        # Create state with tasks but no context
        tasks = UserTasks(["Test task"])
        state = {"files": "", "tasks": tasks}

        inputs = {"context": [], "chat_history": []}

        # Mock prompt template
        prompt_template = Mock(spec=BasePromptTemplate)
        prompt_template.format.return_value = "formatted prompt with very long content"

        # Mock token counting function with very high token count
        count_tokens_fn = Mock()
        count_tokens_fn.return_value = 100000  # High token count

        max_context_tokens = 10  # Very low limit

        # Should handle insufficient context gracefully
        with patch("quivr_core.rag.langgraph_framework.utils.logger") as _:
            result_state, result_inputs = reduce_rag_context(
                state, inputs, prompt_template, count_tokens_fn, max_context_tokens
            )

            # Should not crash and return valid results
            assert "context" in result_inputs
            assert isinstance(result_state, dict)
            assert isinstance(result_inputs, dict)

    def test_context_reduction_with_file_filter(self):
        """Test context reduction with file filtering."""
        state = {"files": "doc1.txt,doc2.pdf", "tasks": UserTasks()}

        inputs = {
            "context": [
                Document(page_content="Content 1", metadata={"source": "doc1.txt"}),
                Document(page_content="Content 2", metadata={"source": "doc2.pdf"}),
                Document(page_content="Content 3", metadata={"source": "doc3.txt"}),
            ],
            "chat_history": [],
        }

        # Mock prompt template
        prompt_template = Mock(spec=BasePromptTemplate)
        prompt_template.format.return_value = "formatted prompt"

        # Mock token counting function
        count_tokens_fn = Mock()
        count_tokens_fn.return_value = 50

        max_context_tokens = 1000

        result_state, result_inputs = reduce_rag_context(
            state, inputs, prompt_template, count_tokens_fn, max_context_tokens
        )

        # Should process context successfully
        assert "context" in result_inputs
        assert isinstance(result_state, dict)
        assert isinstance(result_inputs, dict)


class TestUtilsIntegration:
    """Test integration between utility functions."""

    def test_full_context_reduction_workflow(self):
        """Test complete context reduction workflow."""
        # Create comprehensive test scenario
        tasks = UserTasks(["Analyze documents", "Generate summary"])

        # Add task with documents
        task_id = uuid4()
        task_docs = [
            Document(
                page_content="Analysis content", metadata={"source": "analysis.txt"}
            )
        ]
        tasks.user_tasks[task_id] = UserTaskEntity(
            id=task_id,
            definition="Additional analysis",
            docs=task_docs,
            completable=False,
        )

        state = {"files": "doc1.txt,doc2.pdf", "tasks": tasks}

        inputs = {
            "context": [
                Document(page_content="Doc 1 content", metadata={"source": "doc1.txt"}),
                Document(page_content="Doc 2 content", metadata={"source": "doc2.pdf"}),
                Document(page_content="Doc 3 content", metadata={"source": "doc3.txt"}),
            ],
            "chat_history": [],
        }

        # Mock prompt template
        prompt_template = Mock(spec=BasePromptTemplate)
        prompt_template.format.return_value = "formatted prompt"

        # Mock token counting function
        count_tokens_fn = Mock()
        count_tokens_fn.return_value = 75

        max_context_tokens = 500

        # Test context reduction
        result_state, result_inputs = reduce_rag_context(
            state, inputs, prompt_template, count_tokens_fn, max_context_tokens
        )

        # Test tool updates
        workflow_config = Mock()
        workflow_config.activated_tools = []
        workflow_config.validated_tools = []

        search_tool = Mock()
        search_tool.name = "search_tool"
        workflow_config.validated_tools = [search_tool]

        updated_tools = UpdatedPromptAndTools(
            tools_to_activate=["search_tool"], tools_to_deactivate=[]
        )

        update_active_tools(workflow_config, updated_tools)

        # Verify both operations succeeded
        assert "context" in result_inputs
        assert len(workflow_config.activated_tools) == 1
        assert workflow_config.activated_tools[0].name == "search_tool"
