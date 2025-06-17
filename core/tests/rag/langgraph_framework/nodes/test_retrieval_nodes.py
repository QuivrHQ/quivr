"""Tests for retrieval nodes."""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from langchain_core.documents import Document

from quivr_core.rag.entities.retriever import RetrieverConfig
from quivr_core.rag.entities.reranker import RerankerConfig
from quivr_core.rag.langgraph_framework.nodes.retrieval.retrieve_node import (
    RetrievalNode,
)
from quivr_core.rag.langgraph_framework.nodes.retrieval.dynamic_retrieve_node import (
    DynamicRetrievalNode,
)
from quivr_core.rag.langgraph_framework.nodes.retrieval.compression_retrieve_node import (
    CompressionRetrievalNode,
)
from quivr_core.rag.langgraph_framework.nodes.retrieval.retrieve_full_documents_node import (
    RetrieveFullDocumentsNode,
)
from quivr_core.rag.langgraph_framework.nodes.base.exceptions import NodeValidationError

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
        return RetrievalNode(vector_store=mock_vector_store)

    @pytest.fixture(scope="function")
    def valid_state(self):
        """Create a valid state for testing."""
        state = create_sample_agent_state()
        state["tasks"] = create_sample_user_tasks()
        return state

    def test_node_name_and_config_types(self, retrieve_node):
        """Test node name and configuration types."""
        assert retrieve_node.NODE_NAME == "retrieve"
        assert RetrieverConfig in retrieve_node.CONFIG_TYPES

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

        # Mock the retriever with proper async behavior
        mock_retriever = Mock()
        mock_retriever.ainvoke = AsyncMock(return_value=mock_docs)
        retrieve_node.retriever = mock_retriever

        with patch.object(retrieve_node, "get_config") as mock_get_config:
            mock_get_config.return_value = (RetrieverConfig(), False)

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
        return DynamicRetrievalNode(vector_store=mock_vector_store)

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

        # Mock the retriever with proper async behavior
        mock_retriever = Mock()
        mock_retriever.ainvoke = AsyncMock(return_value=mock_docs)
        dynamic_retrieve_node.retriever = mock_retriever

        with patch.object(dynamic_retrieve_node, "get_config") as mock_get_config:
            mock_get_config.side_effect = [
                (RetrieverConfig(), False),
                (RerankerConfig(), False),
            ]

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
        return CompressionRetrievalNode(vector_store=mock_vector_store)

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

        # Mock the retriever with proper async behavior
        mock_retriever = Mock()
        mock_retriever.ainvoke = AsyncMock(return_value=mock_docs)
        compression_retrieve_node.retriever = mock_retriever

        with patch.object(compression_retrieve_node, "get_config") as mock_get_config:
            mock_get_config.side_effect = [
                (RetrieverConfig(), False),
                (RerankerConfig(), False),
            ]

            _ = await compression_retrieve_node.execute(valid_state)

        # Should have performed retrieval
        mock_retriever.ainvoke.assert_called()


class TestRetrieveFullDocumentsNode:
    """Test RetrieveFullDocumentsNode functionality."""

    @pytest.fixture(scope="function")
    def mock_vector_store(self):
        """Create a mock vector store."""
        mock_store = Mock()
        mock_store.get_vectors_by_knowledge_id = AsyncMock(return_value=[])
        return mock_store

    @pytest.fixture(scope="function")
    def retrieve_full_docs_node(self, mock_vector_store):
        """Create a RetrieveFullDocumentsNode instance."""
        return RetrieveFullDocumentsNode(vector_store=mock_vector_store)

    @pytest.fixture(scope="function")
    def valid_state(self):
        """Create a valid state for testing."""
        state = create_sample_agent_state()
        state["tasks"] = create_sample_user_tasks()
        return state

    def test_node_name(self, retrieve_full_docs_node):
        """Test node name."""
        assert retrieve_full_docs_node.NODE_NAME == "retrieve_full_documents_context"

    def test_validate_input_state_success(self, retrieve_full_docs_node, valid_state):
        """Test successful input state validation."""
        retrieve_full_docs_node.validate_input_state(valid_state)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_with_full_document_retrieval(
        self, retrieve_full_docs_node, valid_state
    ):
        """Test execution with full document retrieval."""
        mock_knowledge_docs = create_knowledge_documents()
        mock_full_docs = [
            Document(
                page_content="Full document content with all pages",
                metadata={"source": "full_doc.txt", "full_document": True},
            )
        ]

        # Set up the tasks to have docs with knowledge_id metadata
        valid_state["tasks"].set_docs(valid_state["tasks"].ids[0], mock_knowledge_docs)

        # Mock the vector store method
        retrieve_full_docs_node.vector_store.get_vectors_by_knowledge_id = AsyncMock(
            return_value=mock_full_docs
        )

        with patch.object(retrieve_full_docs_node, "get_config") as mock_get_config:
            mock_get_config.return_value = (RetrieverConfig(), False)

            result = await retrieve_full_docs_node.execute(valid_state)

        # Should have performed retrieval
        assert result["tasks"] is not None
        retrieve_full_docs_node.vector_store.get_vectors_by_knowledge_id.assert_called()

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_with_no_chunks_found(
        self, retrieve_full_docs_node, valid_state
    ):
        """Test execution when no chunks are found initially."""
        # Clear any existing docs from tasks to simulate no chunks found
        for task_id in valid_state["tasks"].ids:
            valid_state["tasks"].set_docs(task_id, [])

        with patch.object(retrieve_full_docs_node, "get_config") as mock_get_config:
            mock_get_config.return_value = (RetrieverConfig(), False)

            result = await retrieve_full_docs_node.execute(valid_state)

        # Should return state unchanged when no docs
        assert result["tasks"] is not None


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
        return RetrievalNode(vector_store=mock_vector_store)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_with_retrieval_error(self, retrieve_node):
        """Test handling of retrieval errors."""
        state = create_sample_agent_state()
        state["tasks"] = create_sample_user_tasks()

        # Mock retriever to raise an error
        mock_retriever = Mock()
        mock_retriever.ainvoke = AsyncMock(
            side_effect=Exception("Retrieval service unavailable")
        )
        retrieve_node.retriever = mock_retriever

        with patch.object(retrieve_node, "get_config") as mock_get_config:
            mock_get_config.return_value = (RetrieverConfig(), False)

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

    def test_retrieval_nodes_have_proper_dependencies(self, mock_vector_store):
        """Test that retrieval nodes declare proper dependencies."""
        nodes = [
            RetrievalNode(vector_store=mock_vector_store),
            DynamicRetrievalNode(vector_store=mock_vector_store),
            CompressionRetrievalNode(vector_store=mock_vector_store),
        ]

        for node in nodes:
            # All retrieval nodes should have proper node names
            assert hasattr(node, "NODE_NAME")
            assert node.NODE_NAME is not None

            # Should have config types defined
            assert hasattr(node, "CONFIG_TYPES")
            assert RetrieverConfig in node.CONFIG_TYPES
