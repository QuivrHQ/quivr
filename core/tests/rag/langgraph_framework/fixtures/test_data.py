"""Test data fixtures."""

from typing import Dict, Any, List
from uuid import uuid4
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.documents import Document

from quivr_core.rag.entities.chat import ChatHistory
from quivr_core.rag.langgraph_framework.task import UserTasks


def create_sample_agent_state() -> Dict[str, Any]:
    """Create a sample agent state for testing."""
    return {
        "messages": [HumanMessage(content="Hello"), AIMessage(content="Hi there!")],
        "reasoning": ["Initial reasoning step"],
        "chat_history": ChatHistory(brain_id=uuid4(), chat_id=uuid4()),
        "files": "sample_files.txt",
        "tasks": UserTasks(["Sample task"]),
        "instructions": "Follow these instructions",
        "ticket_metadata": {"ticket_id": "123"},
        "user_metadata": {"user_id": "user123"},
        "additional_information": {"context": "test"},
        "tool": "sample_tool",
        "guidelines": "Test guidelines",
        "enforced_system_prompt": "System prompt",
        "_filter": {"type": "test"},
        "ticket_history": "Previous tickets",
    }


def create_sample_user_tasks() -> UserTasks:
    """Create sample user tasks for testing."""
    tasks = UserTasks(
        ["Analyze the document", "Generate a summary", "Answer the question"]
    )

    # Add some documents to the first task
    if tasks.ids:
        task_id = tasks.ids[0]
        docs = [
            Document(
                page_content="Sample document content",
                metadata={"source": "test", "original_file_name": "test.txt"},
            ),
            Document(
                page_content="Another document",
                metadata={"source": "test2", "original_file_name": "test2.txt"},
            ),
        ]
        tasks.set_docs(task_id, docs)

    return tasks


def create_sample_documents() -> List[Document]:
    """Create sample documents for testing."""
    return [
        Document(
            page_content="This is a sample document for testing.",
            metadata={
                "source": "test_doc_1.txt",
                "page": 1,
                "original_file_name": "test_doc_1.txt",
            },
        ),
        Document(
            page_content="This is another sample document with more content for testing purposes.",
            metadata={
                "source": "test_doc_2.txt",
                "page": 1,
                "original_file_name": "test_doc_2.txt",
            },
        ),
        Document(
            page_content="A third document to test document handling and processing.",
            metadata={
                "source": "test_doc_3.txt",
                "page": 1,
                "original_file_name": "test_doc_3.txt",
            },
        ),
    ]


def create_sample_chat_history() -> ChatHistory:
    """Create sample chat history for testing."""
    chat_history = ChatHistory(brain_id=uuid4(), chat_id=uuid4())
    chat_history.append(HumanMessage(content="What is AI?"))
    chat_history.append(AIMessage(content="AI stands for Artificial Intelligence..."))
    chat_history.append(HumanMessage(content="Can you explain more?"))
    return chat_history


# Test configuration data
SAMPLE_GRAPH_CONFIG = {
    "llm_config": {"model": "gpt-3.5-turbo", "temperature": 0.7, "max_tokens": 1000},
    "workflow_config": {"max_iterations": 10, "timeout": 30},
    "nodes": {
        "test_node": {
            "llm_config": {
                "temperature": 0.5  # Override for specific node
            }
        }
    },
}

SAMPLE_NODE_METADATA = {
    "name": "test_node",
    "description": "A test node for unit testing",
    "category": "test",
    "version": "1.0.0",
    "dependencies": ["dep1", "dep2"],
}
