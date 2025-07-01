"""
Enhanced node registry using the unified registry base.

This demonstrates how the existing NodeRegistry can be refactored to use
the new base registry system while maintaining all functionality and
adding enhanced discovery capabilities.
"""

from typing import Type, Optional, List
import logging

from quivr_core.rag.langgraph_framework.base.node import BaseNode
from quivr_core.registry_base import (
    BaseRegistry,
    BaseMetadata,
)

logger = logging.getLogger("quivr_core")


class NodeMetadata(BaseMetadata):
    """Metadata for a registered node."""

    def __init__(
        self,
        node_class: Type[BaseNode],
        name: str,
        dependencies: Optional[List[str]] = None,
        **kwargs,
    ):
        super().__init__(name=name, **kwargs)
        self.node_class = node_class
        self.dependencies = dependencies or []


class NodeRegistry(BaseRegistry[Type[BaseNode], NodeMetadata]):
    """Registry for discovering and managing node types."""

    def _create_metadata(
        self,
        name: str,
        item: Type[BaseNode],
        dependencies: Optional[List[str]] = None,
        **kwargs,
    ) -> NodeMetadata:
        """Create metadata for a node class."""
        return NodeMetadata(
            node_class=item, name=name, dependencies=dependencies, **kwargs
        )

    def _extract_item(self, metadata: NodeMetadata) -> Type[BaseNode]:
        """Extract the node class from metadata."""
        return metadata.node_class

    def create_node(self, name: str, **kwargs) -> BaseNode:
        """Create a node instance by name."""
        node_class = self.get(name)
        return node_class(**kwargs)

    def get_node_dependencies(self, name: str) -> List[str]:
        """Get the dependencies for a node."""
        metadata = self.get_metadata(name)
        return metadata.dependencies

    def list_nodes_by_dependencies(self, dependency: str) -> List[str]:
        """List all nodes that depend on a specific dependency."""
        return [
            name
            for name, metadata in self._items.items()
            if dependency in metadata.dependencies
        ]

    def validate_dependencies(self, name: str) -> bool:
        """Validate that all dependencies for a node are available."""
        metadata = self.get_metadata(name)
        for dep in metadata.dependencies:
            if not self.has_item(dep):
                logger.warning(f"Node {name} has unmet dependency: {dep}")
                return False
        return True

    def get_dependency_graph(self) -> dict[str, List[str]]:
        """Get the full dependency graph for all nodes."""
        return {name: metadata.dependencies for name, metadata in self._items.items()}

    # Legacy method names for backward compatibility
    def register_node(
        self,
        name: str,
        node_class: Type[BaseNode],
        description: str = "",
        category: str = "general",
        version: str = "1.0.0",
        dependencies: Optional[List[str]] = None,
    ) -> None:
        """Legacy method name for node registration."""
        self.register(
            name=name,
            item=node_class,
            description=description,
            category=category,
            version=version,
            dependencies=dependencies,
        )

    def get_node_class(self, name: str) -> Type[BaseNode]:
        """Legacy method name for getting node classes."""
        return self.get(name)

    def get_node_metadata(self, name: str) -> NodeMetadata:
        """Legacy method name for getting node metadata."""
        return self.get_metadata(name)

    def list_nodes(self, category: Optional[str] = None) -> List[str]:
        """Legacy method name for listing nodes."""
        return self.list_items(category=category)


# Global registry instance
node_registry = NodeRegistry()


def enhanced_register_node(
    name: Optional[str] = None,
    description: str = "",
    category: str = "general",
    version: str = "1.0.0",
    dependencies: Optional[List[str]] = None,
    tags: Optional[List[str]] = None,
):
    """Enhanced decorator with dependency and tag support."""

    def decorator(cls: Type[BaseNode]) -> Type[BaseNode]:
        node_name = name or getattr(cls, "NODE_NAME", cls.__name__.lower())

        # Ensure node_name is always a string
        if not isinstance(node_name, str):
            node_name = str(node_name)

        # Store metadata on the class for auto-discovery
        cls._node_metadata = {
            "name": node_name,
            "description": description,
            "category": category,
            "version": version,
            "dependencies": dependencies or [],
            "tags": tags or [],
        }

        # Register immediately if registry is available
        try:
            node_registry.register(
                name=node_name,
                item=cls,
                description=description,
                category=category,
                version=version,
                dependencies=dependencies,
                tags=tags,
            )
        except Exception as e:
            logger.warning(f"Failed to register node {node_name}: {e}")

        return cls

    return decorator


# Use the enhanced decorator as the main decorator since it handles NODE_NAME properly
register_node = enhanced_register_node


# Convenience functions
def get_node_class(name: str) -> Type[BaseNode]:
    """Get a node class by name from the registry."""
    return node_registry.get(name)


def create_node(name: str, **kwargs) -> BaseNode:
    """Create a node instance by name."""
    return node_registry.create_node(name, **kwargs)


def list_available_nodes(category: Optional[str] = None) -> List[str]:
    """List all available nodes, optionally filtered by category."""
    return node_registry.list_items(category=category)


def search_nodes(query: str, categories: Optional[List[str]] = None) -> List[str]:
    """Search for nodes by name or description."""
    return node_registry.search(query, categories)


def validate_node_dependencies(name: str) -> bool:
    """Validate that all dependencies for a node are available."""
    return node_registry.validate_dependencies(name)


def get_dependency_graph() -> dict[str, List[str]]:
    """Get the full dependency graph for all nodes."""
    return node_registry.get_dependency_graph()
