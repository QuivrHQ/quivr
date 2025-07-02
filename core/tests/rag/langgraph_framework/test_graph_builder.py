"""Tests for the GraphBuilder class."""

import pytest
from unittest.mock import Mock, patch
from langgraph.graph import StateGraph

from quivr_core.rag.langgraph_framework.graph_builder import GraphBuilder
from quivr_core.rag.langgraph_framework.registry.node_registry import NodeRegistry

from tests.rag.langgraph_framework.fixtures.mock_nodes import MockNode


class TestGraphBuilderInitialization:
    """Test GraphBuilder initialization."""

    def test_initialization_with_default_registry(self):
        """Test initialization with default registry."""
        builder = GraphBuilder()

        assert builder.registry is not None
        assert isinstance(builder.graph, StateGraph)
        assert builder.nodes == {}

    def test_initialization_with_custom_registry(self):
        """Test initialization with custom registry."""
        custom_registry = Mock(spec=NodeRegistry)
        builder = GraphBuilder(registry=custom_registry)

        assert builder.registry is custom_registry
        assert isinstance(builder.graph, StateGraph)
        assert builder.nodes == {}


class TestGraphBuilderNodeManagement:
    """Test node addition and management."""

    @pytest.fixture(scope="function")
    def mock_registry(self):
        """Create a mock registry with test nodes."""
        registry = Mock(spec=NodeRegistry)
        return registry

    @pytest.fixture(scope="function")
    def builder(self, mock_registry):
        """Create a GraphBuilder with mock registry."""
        return GraphBuilder(registry=mock_registry)

    def test_add_node_success(self, builder, mock_registry):
        """Test successful node addition."""
        mock_node = MockNode()
        mock_registry.create_node.return_value = mock_node

        result = builder.add_node("test_node", "mock_type")

        # Should return self for chaining
        assert result is builder

        # Should create and store node
        mock_registry.create_node.assert_called_once_with("mock_type")
        assert "test_node" in builder.nodes
        assert builder.nodes["test_node"] is mock_node

    def test_add_node_with_kwargs(self, builder, mock_registry):
        """Test node addition with keyword arguments."""
        mock_node = MockNode()
        mock_registry.create_node.return_value = mock_node

        builder.add_node("test_node", "mock_type", param1="value1", param2="value2")

        mock_registry.create_node.assert_called_once_with(
            "mock_type", param1="value1", param2="value2"
        )

    def test_add_node_invalid_type(self, builder, mock_registry):
        """Test error when adding node with invalid type."""
        mock_registry.create_node.side_effect = KeyError("Node type not found")
        mock_registry.list_nodes.return_value = ["valid_type1", "valid_type2"]

        with pytest.raises(ValueError, match="Node type 'invalid_type' not found"):
            builder.add_node("test_node", "invalid_type")

        mock_registry.list_nodes.assert_called_once()

    def test_add_node_logging(self, builder, mock_registry, caplog):
        """Test that node addition is logged."""
        mock_node = MockNode()
        mock_registry.create_node.return_value = mock_node

        builder.add_node("test_node", "mock_type")

        assert "Added node 'test_node' of type 'mock_type'" in caplog.text


class TestGraphBuilderEdgeManagement:
    """Test edge creation and management."""

    @pytest.fixture(scope="function")
    def builder_with_nodes(self):
        """Create a builder with some nodes added."""
        mock_registry = Mock(spec=NodeRegistry)
        mock_registry.create_node.return_value = MockNode()

        builder = GraphBuilder(registry=mock_registry)
        builder.add_node("node1", "mock_type")
        builder.add_node("node2", "mock_type")

        return builder

    def test_add_edge(self, builder_with_nodes):
        """Test adding simple edge."""
        result = builder_with_nodes.add_edge("node1", "node2")

        # Should return self for chaining
        assert result is builder_with_nodes

        # Verify edge was added to graph (we can't easily test this directly,
        # but we can ensure no exceptions were raised)

    def test_add_conditional_edge(self, builder_with_nodes):
        """Test adding conditional edge."""

        def condition_func(state):
            return "next_node"

        condition_map = {"next_node": "node2"}

        result = builder_with_nodes.add_conditional_edge(
            "node1", condition_func, condition_map
        )

        # Should return self for chaining
        assert result is builder_with_nodes


class TestGraphBuilderEntryExitPoints:
    """Test entry and exit point management."""

    @pytest.fixture(scope="function")
    def builder_with_nodes(self):
        """Create a builder with some nodes added."""
        mock_registry = Mock(spec=NodeRegistry)
        mock_registry.create_node.return_value = MockNode()

        builder = GraphBuilder(registry=mock_registry)
        builder.add_node("entry_node", "mock_type")
        builder.add_node("exit_node", "mock_type")

        return builder

    def test_set_entry_point(self, builder_with_nodes):
        """Test setting entry point."""
        result = builder_with_nodes.set_entry_point("entry_node")

        # Should return self for chaining
        assert result is builder_with_nodes

    def test_set_finish_point(self, builder_with_nodes):
        """Test setting finish point."""
        result = builder_with_nodes.set_finish_point("exit_node")

        # Should return self for chaining
        assert result is builder_with_nodes


class TestGraphBuilderChaining:
    """Test builder pattern chaining."""

    def test_method_chaining(self):
        """Test that all methods return self for chaining."""
        mock_registry = Mock(spec=NodeRegistry)
        mock_registry.create_node.return_value = MockNode()

        builder = GraphBuilder(registry=mock_registry)

        # Should be able to chain all operations
        result = (
            builder.add_node("node1", "mock_type")
            .add_node("node2", "mock_type")
            .add_edge("node1", "node2")
            .set_entry_point("node1")
            .set_finish_point("node2")
        )

        assert result is builder


class TestGraphBuilderCompilation:
    """Test graph compilation."""

    def test_build_graph(self):
        """Test building the graph."""
        mock_registry = Mock(spec=NodeRegistry)
        mock_registry.create_node.return_value = MockNode()

        builder = GraphBuilder(registry=mock_registry)
        builder.add_node("test_node", "mock_type")

        # Mock the graph compilation
        mock_compiled_graph = Mock()
        with patch.object(builder.graph, "compile", return_value=mock_compiled_graph):
            result = builder.build()

            assert result is mock_compiled_graph
            builder.graph.compile.assert_called_once()


class TestGraphBuilderUtilities:
    """Test utility methods."""

    def test_list_available_nodes(self):
        """Test listing available nodes by category."""
        mock_registry = Mock(spec=NodeRegistry)
        mock_registry.list_categories.return_value = ["cat1", "cat2"]
        mock_registry.list_nodes.side_effect = lambda cat: {
            "cat1": ["node1", "node2"],
            "cat2": ["node3"],
        }[cat]

        builder = GraphBuilder(registry=mock_registry)
        result = builder.list_available_nodes()

        expected = {"cat1": ["node1", "node2"], "cat2": ["node3"]}
        assert result == expected

        mock_registry.list_categories.assert_called_once()
        assert mock_registry.list_nodes.call_count == 2


class TestCreateRAGWorkflow:
    """Test the example RAG workflow creation function."""

    @patch("quivr_core.rag.langgraph_framework.graph_builder.GraphBuilder")
    def test_create_rag_workflow(self, mock_graph_builder_class):
        """Test the create_rag_workflow example function."""
        from quivr_core.rag.langgraph_framework.graph_builder import create_rag_workflow

        # Setup mocks
        mock_builder = Mock()
        mock_workflow = Mock()

        mock_builder.add_node.return_value = mock_builder
        mock_builder.add_edge.return_value = mock_builder
        mock_builder.set_entry_point.return_value = mock_builder
        mock_builder.set_finish_point.return_value = mock_builder
        mock_builder.build.return_value = mock_workflow

        mock_graph_builder_class.return_value = mock_builder

        # Call function
        result = create_rag_workflow()

        # Verify the workflow was built correctly
        mock_graph_builder_class.assert_called_once()
        mock_builder.add_node.assert_any_call("retrieve", "retrieve")
        mock_builder.add_node.assert_any_call("generate", "generate_rag")
        mock_builder.add_edge.assert_called_once_with("retrieve", "generate")
        mock_builder.set_entry_point.assert_called_once_with("retrieve")
        mock_builder.set_finish_point.assert_called_once_with("generate")
        mock_builder.build.assert_called_once()

        assert result is mock_workflow
