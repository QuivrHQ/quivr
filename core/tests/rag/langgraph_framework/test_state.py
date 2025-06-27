"""Tests for state management functionality."""

import pytest
from uuid import uuid4

from quivr_core.rag.langgraph_framework.state import TasksCompletion, AgentState
from quivr_core.rag.langgraph_framework.task import UserTasks, UserTaskEntity
from quivr_core.rag.entities.chat import ChatHistory


class TestTasksCompletion:
    """Test TasksCompletion model."""

    def test_tasks_completion_minimal(self):
        """Test TasksCompletion with minimal required fields."""
        completion = TasksCompletion(is_task_completable=False, tool=None)

        assert completion.is_task_completable is False
        assert completion.tool is None
        assert completion.is_task_completable_reasoning is None
        assert completion.tool_reasoning is None

    def test_tasks_completion_full(self):
        """Test TasksCompletion with all fields."""
        completion = TasksCompletion(
            is_task_completable=True,
            is_task_completable_reasoning="The task can be completed with available context",
            tool="search_tool",
            tool_reasoning="Search tool is needed to find additional information",
        )

        assert completion.is_task_completable is True
        assert completion.tool == "search_tool"
        assert "available context" in completion.is_task_completable_reasoning
        assert "additional information" in completion.tool_reasoning

    def test_tasks_completion_validation(self):
        """Test TasksCompletion field validation."""
        # Missing required field should raise validation error
        with pytest.raises(ValueError):
            TasksCompletion()  # Missing is_task_completable

    def test_tasks_completion_optional_fields(self):
        """Test TasksCompletion with optional fields only."""
        completion = TasksCompletion(is_task_completable=True, tool="calculator")

        assert completion.is_task_completable is True
        assert completion.tool == "calculator"
        assert completion.is_task_completable_reasoning is None
        assert completion.tool_reasoning is None


class TestAgentState:
    """Test AgentState TypedDict structure."""

    def test_agent_state_creation(self):
        """Test AgentState creation with required fields."""
        chat_id = uuid4()
        brain_id = uuid4()
        chat_history = ChatHistory(chat_id=chat_id, brain_id=brain_id)
        tasks = UserTasks(["Complete analysis"])

        state: AgentState = {
            "messages": [],
            "reasoning": ["Initial reasoning"],
            "chat_history": chat_history,
            "files": "file1.txt, file2.pdf",
            "tasks": tasks,
            "instructions": "Follow the guidelines",
            "ticket_metadata": {"priority": "high"},
            "user_metadata": {"department": "engineering"},
            "additional_information": {"context": "quarterly review"},
            "tool": "search_tool",
            "guidelines": "Be thorough and accurate",
            "enforced_system_prompt": "You are a helpful assistant",
            "_filter": {"type": "document"},
            "ticket_history": "Previous interactions...",
        }

        assert len(state["messages"]) == 0
        assert state["reasoning"] == ["Initial reasoning"]
        assert state["chat_history"] == chat_history
        assert state["files"] == "file1.txt, file2.pdf"
        assert isinstance(state["tasks"], UserTasks)
        assert state["tool"] == "search_tool"

    def test_agent_state_chat_history(self):
        """Test AgentState with ChatHistory integration."""
        chat_id = uuid4()
        brain_id = uuid4()
        chat_history = ChatHistory(chat_id=chat_id, brain_id=brain_id)

        state: AgentState = {
            "messages": [],
            "reasoning": [],
            "chat_history": chat_history,
            "files": "",
            "tasks": UserTasks(),
            "instructions": "",
            "ticket_metadata": None,
            "user_metadata": None,
            "additional_information": None,
            "tool": "",
            "guidelines": "",
            "enforced_system_prompt": "",
            "_filter": None,
            "ticket_history": "",
        }

        assert state["chat_history"].id == chat_id
        assert state["chat_history"].brain_id == brain_id
        assert len(state["chat_history"]) == 0

    def test_agent_state_optional_fields(self):
        """Test AgentState with optional fields set to None."""
        state: AgentState = {
            "messages": [],
            "reasoning": [],
            "chat_history": ChatHistory(chat_id=uuid4(), brain_id=uuid4()),
            "files": "",
            "tasks": UserTasks(),
            "instructions": "",
            "ticket_metadata": None,
            "user_metadata": None,
            "additional_information": None,
            "tool": "",
            "guidelines": "",
            "enforced_system_prompt": "",
            "_filter": None,
            "ticket_history": "",
        }

        assert state["ticket_metadata"] is None
        assert state["user_metadata"] is None
        assert state["additional_information"] is None
        assert state["_filter"] is None


class TestStateIntegration:
    """Test integration between different state components."""

    def test_state_with_tasks_and_completion(self):
        """Test state integration with tasks and completion."""
        # Create tasks
        tasks = UserTasks(["Task 1", "Task 2"])

        # Manually add a task (since UserTasks doesn't have add_task method)
        task_id = uuid4()
        tasks.user_tasks[task_id] = UserTaskEntity(
            id=task_id, definition="Additional task", docs=[], completable=False
        )

        # Create completion
        completion = TasksCompletion(
            is_task_completable=True,
            tool="search_tool",
            is_task_completable_reasoning="Tasks can be completed with search",
            tool_reasoning="Search will provide necessary information",
        )

        # Verify integration
        assert tasks.has_tasks()
        assert len(list(tasks)) == 3  # 2 from constructor + 1 manually added
        assert completion.is_task_completable
        assert completion.tool == "search_tool"

        # Test task manipulation
        tasks.set_completion(task_id, True)
        assert tasks.user_tasks[task_id].completable is True

        tasks.set_tool(task_id, "calculator")
        assert tasks.user_tasks[task_id].tool == "calculator"
