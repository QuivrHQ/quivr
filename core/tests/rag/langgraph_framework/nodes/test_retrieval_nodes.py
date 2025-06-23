"""Tests for retrieval nodes."""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from langchain_core.documents import Document

from quivr_core.rag.langgraph_framework.nodes.retrieval.retrieve_node import (
    RetrievalNode,
)
from quivr_core.rag.langgraph_framework.nodes.retrieval.dynamic_retrieve_node import (
    DynamicRetrievalNode,
)
from quivr_core.rag.langgraph_framework.nodes.retrieval.compression_retrieve_node import (
    CompressionRetrievalNode,
)
from quivr_core.rag.langgraph_framework.base.exceptions import NodeValidationError

from tests.rag.langgraph_framework.fixtures.test_data import (
    create_sample_agent_state,
    create_sample_user_tasks,
    create_sample_documents,
)


def create_knowledge_documents():
    """Create documents with knowledge_id metadata for full document retrieval tests."""
    return [
        Document(
            page_content="This is a sample document for testing.",
            metadata={
                "source": "test_doc_1.txt",
                "knowledge_id": "knowledge_1",
                "chunk_index": 0,
                "similarity": 0.9,
            },
        ),
        Document(
            page_content="This is another sample document with more content for testing purposes.",
            metadata={
                "source": "test_doc_2.txt",
                "knowledge_id": "knowledge_1",
                "chunk_index": 1,
                "similarity": 0.8,
            },
        ),
        Document(
            page_content="A third document to test document handling and processing.",
            metadata={
                "source": "test_doc_3.txt",
                "knowledge_id": "knowledge_2",
                "chunk_index": 0,
                "similarity": 0.7,
            },
        ),
    ]


class TestRetrieveNode:
    """Test basic RetrieveNode functionality."""

    @pytest.fixture(scope="function")
    def mock_vector_store(self):
        """Create a mock vector store."""
        mock_store = Mock()
        mock_store.as_retriever.return_value = Mock()
        return mock_store

    @pytest.fixture(scope="function")
    def retrieve_node(self, mock_vector_store):
        """Create a RetrieveNode instance."""
        from quivr_core.rag.langgraph_framework.services.service_container import (
            ServiceContainer,
        )

        service_container = ServiceContainer(vector_store=mock_vector_store)
        return RetrievalNode(service_container=service_container)

    @pytest.fixture(scope="function")
    def valid_state(self):
        """Create a valid state for testing."""
        state = create_sample_agent_state()
        state["tasks"] = create_sample_user_tasks()
        return state

    def test_node_name(self, retrieve_node):
        """Test node name and configuration types."""
        assert retrieve_node.NODE_NAME == "retrieve"

    def test_validate_input_state_success(self, retrieve_node, valid_state):
        """Test successful input state validation."""
        retrieve_node.validate_input_state(valid_state)

    def test_validate_input_state_missing_messages(self, retrieve_node):
        """Test input validation with missing messages."""
        state = {"tasks": create_sample_user_tasks()}

        with pytest.raises(NodeValidationError, match="requires 'messages' attribute"):
            retrieve_node.validate_input_state(state)

    def test_validate_input_state_empty_messages(self, retrieve_node):
        """Test input validation with empty messages."""
        state = {"messages": [], "tasks": create_sample_user_tasks()}

        with pytest.raises(NodeValidationError, match="requires non-empty messages"):
            retrieve_node.validate_input_state(state)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_success(self, retrieve_node, valid_state):
        """Test successful execution."""
        mock_docs = create_sample_documents()

        # Mock the retrieval service methods instead of setting retriever attribute
        with patch.object(retrieve_node, "get_service") as mock_get_service:
            mock_retrieval_service = Mock()
            mock_retriever = Mock()
            mock_retriever.ainvoke = AsyncMock(return_value=mock_docs)
            mock_retrieval_service.get_basic_retriever.return_value = mock_retriever
            mock_get_service.return_value = mock_retrieval_service

            result = await retrieve_node.execute(valid_state)

        # Check that documents were set in tasks
        assert result["tasks"] is not None
        mock_retriever.ainvoke.assert_called()


class TestDynamicRetrieveNode:
    """Test DynamicRetrieveNode functionality."""

    @pytest.fixture(scope="function")
    def mock_vector_store(self):
        """Create a mock vector store."""
        mock_store = Mock()
        mock_store.as_retriever.return_value = Mock()
        return mock_store

    @pytest.fixture(scope="function")
    def dynamic_retrieve_node(self, mock_vector_store):
        """Create a DynamicRetrieveNode instance."""
        from quivr_core.rag.langgraph_framework.services.service_container import (
            ServiceContainer,
        )

        service_container = ServiceContainer(vector_store=mock_vector_store)
        return DynamicRetrievalNode(service_container=service_container)

    @pytest.fixture(scope="function")
    def valid_state(self):
        """Create a valid state for testing."""
        state = create_sample_agent_state()
        state["tasks"] = create_sample_user_tasks()
        return state

    def test_node_name(self, dynamic_retrieve_node):
        """Test node name."""
        assert dynamic_retrieve_node.NODE_NAME == "dynamic_retrieve"

    def test_validate_input_state_success(self, dynamic_retrieve_node, valid_state):
        """Test successful input state validation."""
        dynamic_retrieve_node.validate_input_state(valid_state)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_with_retrieval_needed(
        self, dynamic_retrieve_node, valid_state
    ):
        """Test execution when retrieval is needed."""
        mock_docs = create_sample_documents()

        # Mock the retrieval service methods for compression retriever
        with patch.object(dynamic_retrieve_node, "get_service") as mock_get_service:
            mock_retrieval_service = Mock()
            mock_retriever = Mock()
            mock_retriever.ainvoke = AsyncMock(return_value=mock_docs)
            mock_retrieval_service.get_compression_retriever.return_value = (
                mock_retriever
            )
            mock_get_service.return_value = mock_retrieval_service

            _ = await dynamic_retrieve_node.execute(valid_state)

        # Should have performed retrieval
        mock_retriever.ainvoke.assert_called()


class TestCompressionRetrieveNode:
    """Test CompressionRetrieveNode functionality."""

    @pytest.fixture(scope="function")
    def mock_vector_store(self):
        """Create a mock vector store."""
        mock_store = Mock()
        mock_store.as_retriever.return_value = Mock()
        return mock_store

    @pytest.fixture(scope="function")
    def compression_retrieve_node(self, mock_vector_store):
        """Create a CompressionRetrieveNode instance."""
        from quivr_core.rag.langgraph_framework.services.service_container import (
            ServiceContainer,
        )

        service_container = ServiceContainer(vector_store=mock_vector_store)
        return CompressionRetrievalNode(service_container=service_container)

    @pytest.fixture(scope="function")
    def valid_state(self):
        """Create a valid state for testing."""
        state = create_sample_agent_state()
        state["tasks"] = create_sample_user_tasks()
        return state

    def test_node_name(self, compression_retrieve_node):
        """Test node name."""
        assert compression_retrieve_node.NODE_NAME == "compression_retrieve"

    def test_validate_input_state_success(self, compression_retrieve_node, valid_state):
        """Test successful input state validation."""
        compression_retrieve_node.validate_input_state(valid_state)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_with_compression(
        self, compression_retrieve_node, valid_state
    ):
        """Test execution with document compression."""
        mock_docs = create_sample_documents()

        # Mock the retrieval service methods for compression retriever
        with patch.object(compression_retrieve_node, "get_service") as mock_get_service:
            mock_retrieval_service = Mock()
            mock_retriever = Mock()
            mock_retriever.ainvoke = AsyncMock(return_value=mock_docs)
            mock_retrieval_service.get_compression_retriever.return_value = (
                mock_retriever
            )
            mock_get_service.return_value = mock_retrieval_service

            _ = await compression_retrieve_node.execute(valid_state)

        # Should have performed retrieval
        mock_retriever.ainvoke.assert_called()


class TestRetrievalNodeErrorHandling:
    """Test error handling across retrieval nodes."""

    @pytest.fixture(scope="function")
    def mock_vector_store(self):
        """Create a mock vector store."""
        mock_store = Mock()
        mock_store.as_retriever.return_value = Mock()
        return mock_store

    @pytest.fixture(scope="function")
    def retrieve_node(self, mock_vector_store):
        """Create a RetrieveNode instance."""
        from quivr_core.rag.langgraph_framework.services.service_container import (
            ServiceContainer,
        )

        service_container = ServiceContainer(vector_store=mock_vector_store)
        return RetrievalNode(service_container=service_container)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_with_retrieval_error(self, retrieve_node):
        """Test handling of retrieval errors."""
        state = create_sample_agent_state()
        state["tasks"] = create_sample_user_tasks()

        # Mock the retrieval service to raise an error
        with patch.object(retrieve_node, "get_service") as mock_get_service:
            mock_retrieval_service = Mock()
            mock_retriever = Mock()
            mock_retriever.ainvoke = AsyncMock(
                side_effect=Exception("Retrieval service unavailable")
            )
            mock_retrieval_service.get_basic_retriever.return_value = mock_retriever
            mock_get_service.return_value = mock_retrieval_service

            with pytest.raises(Exception, match="Retrieval service unavailable"):
                await retrieve_node.execute(state)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_with_config_error(self, retrieve_node):
        """Test handling of configuration errors."""
        state = create_sample_agent_state()
        state["tasks"] = create_sample_user_tasks()

        with patch.object(retrieve_node, "get_config") as mock_get_config:
            mock_get_config.side_effect = Exception("Invalid configuration")

            with pytest.raises(Exception, match="Invalid configuration"):
                await retrieve_node.execute(state)


class TestRetrievalNodeIntegration:
    """Test integration aspects of retrieval nodes."""

    @pytest.fixture(scope="function")
    def mock_vector_store(self):
        """Create a mock vector store."""
        mock_store = Mock()
        mock_store.as_retriever.return_value = Mock()
        return mock_store

    def test_all_retrieval_nodes_registered(self):
        """Test that all retrieval nodes are properly registered."""
        from quivr_core.rag.langgraph_framework.registry.node_registry import (
            node_registry,
        )

        retrieval_nodes = node_registry.list_nodes("retrieval")

        expected_nodes = [
            "retrieve",
            "dynamic_retrieve",
            "compression_retrieve",
        ]

        # Check that expected nodes are registered
        for expected_node in expected_nodes:
            assert (
                expected_node in retrieval_nodes
            ), f"Node {expected_node} not registered"

    def test_retrieval_nodes_have_proper_dependencies(self):
        """Test that retrieval nodes declare proper dependencies."""
        nodes = [
            RetrievalNode(),
            DynamicRetrievalNode(),
            CompressionRetrievalNode(),
        ]

        for node in nodes:
            # All retrieval nodes should have proper node names
            assert hasattr(node, "NODE_NAME")
            assert node.NODE_NAME is not None
