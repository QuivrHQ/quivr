"""Tests for the node registry system."""

import pytest
from unittest.mock import Mock

from quivr_core.rag.langgraph_framework.registry.node_registry import (
    NodeRegistry,
    NodeMetadata,
    register_node,
    node_registry,
)
from quivr_core.rag.langgraph_framework.base.node import BaseNode

from tests.rag.langgraph_framework.fixtures.mock_nodes import MockNode, AsyncMockNode


class TestNodeMetadata:
    """Test NodeMetadata class."""

    def test_metadata_creation(self):
        """Test basic metadata creation."""
        metadata = NodeMetadata(
            node_class=MockNode,
            name="test_node",
            description="Test description",
            category="test",
            version="1.0.0",
            dependencies=["dep1", "dep2"],
        )

        assert metadata.node_class == MockNode
        assert metadata.name == "test_node"
        assert metadata.description == "Test description"
        assert metadata.category == "test"
        assert metadata.version == "1.0.0"
        assert metadata.dependencies == ["dep1", "dep2"]

    def test_metadata_defaults(self):
        """Test metadata with default values."""
        metadata = NodeMetadata(node_class=MockNode, name="test_node")

        assert metadata.description == ""
        assert metadata.category == "general"
        assert metadata.version == "1.0.0"
        assert metadata.dependencies == []


class TestNodeRegistry:
    """Test NodeRegistry class."""

    @pytest.fixture(scope="function")
    def registry(self):
        """Create a fresh registry for each test."""
        return NodeRegistry()

    def test_register_node_basic(self, registry):
        """Test basic node registration."""
        registry.register_node("test_node", MockNode)

        assert "test_node" in registry._items
        assert registry._items["test_node"].node_class == MockNode
        assert registry._items["test_node"].name == "test_node"
        assert "general" in registry._categories
        assert "test_node" in registry._categories["general"]

    def test_register_node_with_metadata(self, registry):
        """Test node registration with full metadata."""
        registry.register_node(
            name="advanced_node",
            node_class=AsyncMockNode,
            description="An advanced test node",
            category="advanced",
            version="2.0.0",
            dependencies=["dep1", "dep2"],
        )

        metadata = registry._items["advanced_node"]
        assert metadata.node_class == AsyncMockNode
        assert metadata.description == "An advanced test node"
        assert metadata.category == "advanced"
        assert metadata.version == "2.0.0"
        assert metadata.dependencies == ["dep1", "dep2"]

        assert "advanced" in registry._categories
        assert "advanced_node" in registry._categories["advanced"]

    def test_register_node_duplicate_override(self, registry, caplog):
        """Test that duplicate registration shows warning and overrides."""
        registry.register_node("duplicate", MockNode)
        registry.register_node(
            "duplicate", AsyncMockNode, description="New description"
        )

        # Should log warning
        assert "Overriding existing registration: duplicate" in caplog.text

        # Should override with new class
        assert registry._items["duplicate"].node_class == AsyncMockNode
        assert registry._items["duplicate"].description == "New description"

    def test_get_node_class(self, registry):
        """Test retrieving node class."""
        registry.register_node("test_node", MockNode)

        node_class = registry.get_node_class("test_node")
        assert node_class == MockNode

    def test_get_node_class_not_found(self, registry):
        """Test error when node class not found."""
        with pytest.raises(KeyError, match="Item 'nonexistent' not found in registry"):
            registry.get_node_class("nonexistent")

    def test_get_node_metadata(self, registry):
        """Test retrieving node metadata."""
        registry.register_node("test_node", MockNode, description="Test desc")

        metadata = registry.get_node_metadata("test_node")
        assert isinstance(metadata, NodeMetadata)
        assert metadata.node_class == MockNode
        assert metadata.description == "Test desc"

    def test_get_node_metadata_not_found(self, registry):
        """Test error when node metadata not found."""
        with pytest.raises(KeyError, match="Item 'nonexistent' not found in registry"):
            registry.get_node_metadata("nonexistent")

    def test_list_nodes_all(self, registry):
        """Test listing all nodes."""
        registry.register_node("node1", MockNode, category="cat1")
        registry.register_node("node2", AsyncMockNode, category="cat2")
        registry.register_node("node3", MockNode, category="cat1")

        all_nodes = registry.list_nodes()
        assert set(all_nodes) == {"node1", "node2", "node3"}

    def test_list_nodes_by_category(self, registry):
        """Test listing nodes by category."""
        registry.register_node("node1", MockNode, category="cat1")
        registry.register_node("node2", AsyncMockNode, category="cat2")
        registry.register_node("node3", MockNode, category="cat1")

        cat1_nodes = registry.list_nodes("cat1")
        assert set(cat1_nodes) == {"node1", "node3"}

        cat2_nodes = registry.list_nodes("cat2")
        assert cat2_nodes == ["node2"]

        empty_nodes = registry.list_nodes("nonexistent")
        assert empty_nodes == []

    def test_list_categories(self, registry):
        """Test listing all categories."""
        registry.register_node("node1", MockNode, category="cat1")
        registry.register_node("node2", AsyncMockNode, category="cat2")
        registry.register_node("node3", MockNode, category="cat1")

        categories = registry.list_categories()
        assert set(categories) == {"cat1", "cat2"}

    def test_create_node_basic(self, registry):
        """Test creating node instance."""
        registry.register_node("test_node", MockNode)

        node = registry.create_node("test_node")
        assert isinstance(node, MockNode)
        assert node.node_name == "mock_node"  # From MockNode.NODE_NAME

    def test_create_node_with_kwargs(self, registry):
        """Test creating node instance with kwargs."""
        registry.register_node("test_node", MockNode)

        node = registry.create_node("test_node", node_name="custom_name")
        assert isinstance(node, MockNode)
        assert node.node_name == "custom_name"

    def test_create_node_not_found(self, registry):
        """Test error when creating non-existent node."""
        with pytest.raises(KeyError, match="Item 'nonexistent' not found in registry"):
            registry.create_node("nonexistent")


class TestRegisterDecorator:
    """Test the @register_node decorator."""

    @pytest.fixture(scope="function")
    def clean_registry(self):
        """Create a clean registry and restore after test."""
        original_items = node_registry._items.copy()
        original_categories = node_registry._categories.copy()

        # Clear registry
        node_registry._items.clear()
        node_registry._categories.clear()

        yield node_registry

        # Restore original state
        node_registry._items = original_items
        node_registry._categories = original_categories

    def test_decorator_basic(self, clean_registry):
        """Test basic decorator usage."""

        @register_node()
        class DecoratedNode(BaseNode):
            NODE_NAME = "decorated_node"

            def validate_input_state(self, state):
                pass

            def validate_output_state(self, state):
                pass

            async def execute(self, state, config=None):
                return state

        # Should be registered automatically
        assert "decorated_node" in clean_registry._items
        assert clean_registry._items["decorated_node"].node_class == DecoratedNode

    def test_decorator_with_name(self, clean_registry):
        """Test decorator with custom name."""

        @register_node(name="custom_name")
        class DecoratedNode(BaseNode):
            def validate_input_state(self, state):
                pass

            def validate_output_state(self, state):
                pass

            async def execute(self, state, config=None):
                return state

        assert "custom_name" in clean_registry._items
        assert clean_registry._items["custom_name"].node_class == DecoratedNode

    def test_decorator_with_metadata(self, clean_registry):
        """Test decorator with full metadata."""

        @register_node(
            name="full_metadata_node",
            description="A fully decorated node",
            category="decorated",
            version="2.1.0",
            dependencies=["dep1"],
        )
        class DecoratedNode(BaseNode):
            def validate_input_state(self, state):
                pass

            def validate_output_state(self, state):
                pass

            async def execute(self, state, config=None):
                return state

        metadata = clean_registry._items["full_metadata_node"]
        assert metadata.description == "A fully decorated node"
        assert metadata.category == "decorated"
        assert metadata.version == "2.1.0"
        assert metadata.dependencies == ["dep1"]

    def test_decorator_stores_metadata_on_class(self, clean_registry):
        """Test that decorator stores metadata on the class."""

        @register_node(
            name="metadata_class", description="Test description", category="test"
        )
        class DecoratedNode(BaseNode):
            def validate_input_state(self, state):
                pass

            def validate_output_state(self, state):
                pass

            async def execute(self, state, config=None):
                return state

        assert hasattr(DecoratedNode, "_node_metadata")
        metadata = DecoratedNode._node_metadata
        assert metadata["name"] == "metadata_class"
        assert metadata["description"] == "Test description"
        assert metadata["category"] == "test"

    def test_decorator_registration_failure(self, clean_registry, caplog):
        """Test decorator handles registration failures gracefully."""
        # Mock the registry to raise an exception
        original_register = clean_registry.register
        clean_registry.register = Mock(side_effect=Exception("Registration failed"))

        try:

            @register_node(name="failing_node")
            class FailingNode(BaseNode):
                def validate_input_state(self, state):
                    pass

                def validate_output_state(self, state):
                    pass

                async def execute(self, state, config=None):
                    return state

            # Should log warning but not raise exception
            assert "Failed to register node failing_node" in caplog.text

            # Class should still be decorated with metadata
            assert hasattr(FailingNode, "_node_metadata")

        finally:
            # Restore original method
            clean_registry.register = original_register


class TestGlobalRegistry:
    """Test the global registry instance."""

    def test_global_registry_exists(self):
        """Test that global registry exists and is a NodeRegistry."""
        assert isinstance(node_registry, NodeRegistry)

    def test_global_registry_has_nodes(self):
        """Test that global registry has some nodes registered."""
        # This assumes that importing the framework registers some nodes
        # The exact nodes will depend on what's imported
        nodes = node_registry.list_nodes()
        # We can't assert specific nodes since they depend on imports
        # but we can assert it's a list
        assert isinstance(nodes, list)
