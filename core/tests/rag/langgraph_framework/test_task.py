"""Tests for task management functionality."""

import pytest
from uuid import uuid4
from langchain_core.documents import Document

from quivr_core.rag.langgraph_framework.task import UserTaskEntity, UserTasks


class TestUserTaskEntity:
    """Test UserTaskEntity model."""

    def test_user_task_entity_creation(self):
        """Test basic UserTaskEntity creation."""
        task_id = uuid4()
        task = UserTaskEntity(
            id=task_id,
            definition="Complete the analysis",
            docs=[],
            completable=False,
            tool=None,
        )

        assert task.id == task_id
        assert task.definition == "Complete the analysis"
        assert task.docs == []
        assert task.completable is False
        assert task.tool is None

    def test_user_task_entity_with_documents(self):
        """Test UserTaskEntity with documents."""
        task_id = uuid4()
        docs = [
            Document(page_content="Test content", metadata={"source": "test"}),
            Document(page_content="More content", metadata={"source": "test2"}),
        ]

        task = UserTaskEntity(
            id=task_id,
            definition="Analyze documents",
            docs=docs,
            completable=True,
            tool="analyzer",
        )

        assert len(task.docs) == 2
        assert task.docs[0].page_content == "Test content"
        assert task.completable is True
        assert task.tool == "analyzer"

    def test_user_task_entity_defaults(self):
        """Test UserTaskEntity with default values."""
        task_id = uuid4()
        task = UserTaskEntity(id=task_id, definition="Test task")

        assert task.docs == []
        assert task.completable is False
        assert task.tool is None

    def test_has_tool_method(self):
        """Test has_tool method."""
        task_id = uuid4()

        # Task without tool
        task_without_tool = UserTaskEntity(id=task_id, definition="Test")
        assert task_without_tool.has_tool() is False

        # Task with tool
        task_with_tool = UserTaskEntity(id=task_id, definition="Test", tool="search")
        assert task_with_tool.has_tool() is True

        # Task with empty string tool
        task_empty_tool = UserTaskEntity(id=task_id, definition="Test", tool="")
        assert task_empty_tool.has_tool() is False

    def test_is_completable_method(self):
        """Test is_completable method."""
        task_id = uuid4()

        # Non-completable task
        task_not_completable = UserTaskEntity(
            id=task_id, definition="Test", completable=False
        )
        assert task_not_completable.is_completable() is False

        # Completable task
        task_completable = UserTaskEntity(
            id=task_id, definition="Test", completable=True
        )
        assert task_completable.is_completable() is True


class TestUserTasks:
    """Test UserTasks collection."""

    def test_user_tasks_empty_initialization(self):
        """Test UserTasks initialization with no tasks."""
        tasks = UserTasks()

        assert not tasks.has_tasks()
        assert len(tasks.user_tasks) == 0
        assert tasks.ids == []
        assert tasks.definitions == []
        assert tasks.docs == []

    def test_user_tasks_initialization_with_definitions(self):
        """Test UserTasks initialization with task definitions."""
        definitions = ["Task 1", "Task 2", "Task 3"]
        tasks = UserTasks(task_definitions=definitions)

        assert tasks.has_tasks()
        assert len(tasks.user_tasks) == 3
        assert len(tasks.ids) == 3
        assert tasks.definitions == definitions

        # All tasks should be non-completable by default
        for task in tasks:
            assert not task.is_completable()
            assert not task.has_tool()

    def test_user_tasks_iteration(self):
        """Test UserTasks iteration."""
        definitions = ["Task 1", "Task 2"]
        tasks = UserTasks(task_definitions=definitions)

        task_list = list(tasks)
        assert len(task_list) == 2
        assert all(isinstance(task, UserTaskEntity) for task in task_list)
        assert task_list[0].definition == "Task 1"
        assert task_list[1].definition == "Task 2"

    def test_set_docs(self):
        """Test setting documents for a task."""
        tasks = UserTasks(task_definitions=["Test task"])
        task_id = tasks.ids[0]

        docs = [
            Document(page_content="Content 1", metadata={"source": "doc1"}),
            Document(page_content="Content 2", metadata={"source": "doc2"}),
        ]

        tasks.set_docs(task_id, docs)

        task = tasks(task_id)
        assert len(task.docs) == 2
        assert task.docs[0].page_content == "Content 1"
        assert task.docs[1].page_content == "Content 2"

    def test_set_docs_invalid_id(self):
        """Test setting documents with invalid task ID."""
        tasks = UserTasks(task_definitions=["Test task"])
        invalid_id = uuid4()

        with pytest.raises(ValueError, match=f"Task with id {invalid_id} not found"):
            tasks.set_docs(invalid_id, [])

    def test_set_docs_empty_tasks(self):
        """Test setting documents when no tasks exist."""
        tasks = UserTasks()  # No tasks
        task_id = uuid4()

        # Should not raise error but also not do anything
        tasks.set_docs(task_id, [])

    def test_set_definition(self):
        """Test setting task definition."""
        tasks = UserTasks(task_definitions=["Original task"])
        task_id = tasks.ids[0]

        tasks.set_definition(task_id, "Updated task definition")

        task = tasks(task_id)
        assert task.definition == "Updated task definition"

    def test_set_definition_invalid_id(self):
        """Test setting definition with invalid task ID."""
        tasks = UserTasks(task_definitions=["Test task"])
        invalid_id = uuid4()

        with pytest.raises(ValueError, match=f"Task with id {invalid_id} not found"):
            tasks.set_definition(invalid_id, "New definition")

    def test_set_completion(self):
        """Test setting task completion status."""
        tasks = UserTasks(task_definitions=["Test task"])
        task_id = tasks.ids[0]

        # Initially not completable
        assert not tasks(task_id).is_completable()

        # Set as completable
        tasks.set_completion(task_id, True)
        assert tasks(task_id).is_completable()

        # Set back to not completable
        tasks.set_completion(task_id, False)
        assert not tasks(task_id).is_completable()

    def test_set_completion_invalid_id(self):
        """Test setting completion with invalid task ID."""
        tasks = UserTasks(task_definitions=["Test task"])
        invalid_id = uuid4()

        with pytest.raises(ValueError, match=f"Task with id {invalid_id} not found"):
            tasks.set_completion(invalid_id, True)

    def test_set_tool(self):
        """Test setting task tool."""
        tasks = UserTasks(task_definitions=["Test task"])
        task_id = tasks.ids[0]

        # Initially no tool
        assert not tasks(task_id).has_tool()

        # Set tool
        tasks.set_tool(task_id, "search_tool")
        assert tasks(task_id).has_tool()
        assert tasks(task_id).tool == "search_tool"

    def test_set_tool_invalid_id(self):
        """Test setting tool with invalid task ID."""
        tasks = UserTasks(task_definitions=["Test task"])
        invalid_id = uuid4()

        with pytest.raises(ValueError, match=f"Task with id {invalid_id} not found"):
            tasks.set_tool(invalid_id, "tool")

    def test_call_method(self):
        """Test calling UserTasks to get specific task."""
        tasks = UserTasks(task_definitions=["Task 1", "Task 2"])
        task_id = tasks.ids[0]

        task = tasks(task_id)
        assert isinstance(task, UserTaskEntity)
        assert task.definition == "Task 1"
        assert task.id == task_id

    def test_has_non_completable_tasks(self):
        """Test has_non_completable_tasks method."""
        tasks = UserTasks(task_definitions=["Task 1", "Task 2", "Task 3"])

        # Initially all tasks are non-completable
        assert tasks.has_non_completable_tasks()

        # Mark some as completable
        tasks.set_completion(tasks.ids[0], True)
        tasks.set_completion(tasks.ids[1], True)

        # Still has one non-completable task
        assert tasks.has_non_completable_tasks()

        # Mark all as completable
        tasks.set_completion(tasks.ids[2], True)

        # No more non-completable tasks
        assert not tasks.has_non_completable_tasks()

    def test_non_completable_tasks_property(self):
        """Test non_completable_tasks property."""
        tasks = UserTasks(task_definitions=["Task 1", "Task 2", "Task 3"])

        # Initially all are non-completable
        non_completable = tasks.non_completable_tasks
        assert len(non_completable) == 3

        # Mark one as completable
        tasks.set_completion(tasks.ids[0], True)
        non_completable = tasks.non_completable_tasks
        assert len(non_completable) == 2

        # Mark all as completable
        for task_id in tasks.ids:
            tasks.set_completion(task_id, True)

        non_completable = tasks.non_completable_tasks
        assert len(non_completable) == 0

    def test_completable_tasks_property(self):
        """Test completable_tasks property."""
        tasks = UserTasks(task_definitions=["Task 1", "Task 2", "Task 3"])

        # Initially none are completable
        completable = tasks.completable_tasks
        assert len(completable) == 0

        # Mark one as completable
        tasks.set_completion(tasks.ids[0], True)
        completable = tasks.completable_tasks
        assert len(completable) == 1
        assert completable[0].definition == "Task 1"

        # Mark all as completable
        for task_id in tasks.ids:
            tasks.set_completion(task_id, True)

        completable = tasks.completable_tasks
        assert len(completable) == 3

    def test_docs_property(self):
        """Test docs property that concatenates all task docs."""
        tasks = UserTasks(task_definitions=["Task 1", "Task 2"])

        # Initially no docs
        assert tasks.docs == []

        # Add docs to first task
        docs1 = [
            Document(page_content="Doc 1 for task 1", metadata={"task": 1}),
            Document(page_content="Doc 2 for task 1", metadata={"task": 1}),
        ]
        tasks.set_docs(tasks.ids[0], docs1)

        # Add docs to second task
        docs2 = [Document(page_content="Doc 1 for task 2", metadata={"task": 2})]
        tasks.set_docs(tasks.ids[1], docs2)

        # Should concatenate all docs
        all_docs = tasks.docs
        assert len(all_docs) == 3
        assert all_docs[0].page_content == "Doc 1 for task 1"
        assert all_docs[1].page_content == "Doc 2 for task 1"
        assert all_docs[2].page_content == "Doc 1 for task 2"


class TestUserTasksIntegration:
    """Test UserTasks integration scenarios."""

    def test_complex_task_workflow(self):
        """Test a complex workflow with multiple operations."""
        # Create tasks
        tasks = UserTasks(
            task_definitions=[
                "Analyze the financial report",
                "Generate summary",
                "Create recommendations",
            ]
        )

        # Add documents to analysis task
        analysis_docs = [
            Document(page_content="Q1 Revenue: $1M", metadata={"type": "financial"}),
            Document(page_content="Q1 Expenses: $800K", metadata={"type": "financial"}),
        ]
        tasks.set_docs(tasks.ids[0], analysis_docs)

        # Set tools for different tasks
        tasks.set_tool(tasks.ids[0], "financial_analyzer")
        tasks.set_tool(tasks.ids[1], "summarizer")
        tasks.set_tool(tasks.ids[2], "recommendation_engine")

        # Complete first task
        tasks.set_completion(tasks.ids[0], True)

        # Verify state
        assert tasks.has_non_completable_tasks()
        assert len(tasks.completable_tasks) == 1
        assert len(tasks.non_completable_tasks) == 2
        assert len(tasks.docs) == 2  # From first task

        # Complete all tasks
        for task_id in tasks.ids[1:]:
            tasks.set_completion(task_id, True)

        # All should be complete now
        assert not tasks.has_non_completable_tasks()
        assert len(tasks.completable_tasks) == 3
        assert all(task.has_tool() for task in tasks)

    def test_task_modification_workflow(self):
        """Test modifying tasks after creation."""
        tasks = UserTasks(task_definitions=["Original task"])
        task_id = tasks.ids[0]

        # Modify definition
        tasks.set_definition(task_id, "Updated task definition")

        # Add documents
        docs = [Document(page_content="New document", metadata={"source": "update"})]
        tasks.set_docs(task_id, docs)

        # Set tool and complete
        tasks.set_tool(task_id, "updated_tool")
        tasks.set_completion(task_id, True)

        # Verify all changes
        task = tasks(task_id)
        assert task.definition == "Updated task definition"
        assert len(task.docs) == 1
        assert task.docs[0].page_content == "New document"
        assert task.tool == "updated_tool"
        assert task.is_completable()

    def test_empty_tasks_edge_cases(self):
        """Test edge cases with empty tasks."""
        tasks = UserTasks()

        # All properties should work with empty tasks
        assert not tasks.has_tasks()
        assert not tasks.has_non_completable_tasks()
        assert tasks.ids == []
        assert tasks.definitions == []
        assert tasks.docs == []
        assert tasks.completable_tasks == []
        assert tasks.non_completable_tasks == []

        # Iteration should work
        task_list = list(tasks)
        assert task_list == []
