from typing import Dict, Type, List, Optional
import logging

from quivr_core.rag.langgraph_framework.base.node import BaseNode

logger = logging.getLogger("quivr_core")


class NodeMetadata:
    """Metadata for a registered node."""

    def __init__(
        self,
        node_class: Type[BaseNode],
        name: str,
        description: str = "",
        category: str = "general",
        version: str = "1.0.0",
        dependencies: Optional[List[str]] = None,
    ):
        self.node_class = node_class
        self.name = name
        self.description = description
        self.category = category
        self.version = version
        self.dependencies = dependencies or []


class NodeRegistry:
    """Registry for discovering and managing node types."""

    def __init__(self):
        self._nodes: Dict[str, NodeMetadata] = {}
        self._categories: Dict[str, List[str]] = {}

    def register_node(
        self,
        name: str,
        node_class: Type[BaseNode],
        description: str = "",
        category: str = "general",
        version: str = "1.0.0",
        dependencies: Optional[List[str]] = None,
    ) -> None:
        """Register a node type."""

        if name in self._nodes:
            logger.warning(f"Overriding existing node registration: {name}")

        metadata = NodeMetadata(
            node_class=node_class,
            name=name,
            description=description,
            category=category,
            version=version,
            dependencies=dependencies,
        )

        self._nodes[name] = metadata

        # Update category index
        if category not in self._categories:
            self._categories[category] = []
        if name not in self._categories[category]:
            self._categories[category].append(name)

        logger.info(f"Registered node: {name} (category: {category})")

    def get_node_class(self, name: str) -> Type[BaseNode]:
        """Get a node class by name."""
        if name not in self._nodes:
            raise KeyError(f"Node '{name}' not found in registry")
        return self._nodes[name].node_class

    def get_node_metadata(self, name: str) -> NodeMetadata:
        """Get node metadata by name."""
        if name not in self._nodes:
            raise KeyError(f"Node '{name}' not found in registry")
        return self._nodes[name]

    def list_nodes(self, category: Optional[str] = None) -> List[str]:
        """List all registered node names, optionally filtered by category."""
        if category:
            return self._categories.get(category, [])
        return list(self._nodes.keys())

    def list_categories(self) -> List[str]:
        """List all available categories."""
        return list(self._categories.keys())

    def create_node(self, name: str, **kwargs) -> BaseNode:
        """Create a node instance by name."""
        node_class = self.get_node_class(name)
        return node_class(**kwargs)


# Global registry instance
node_registry = NodeRegistry()


# Decorator for easy node registration
def register_node(
    name: Optional[str] = None,
    description: str = "",
    category: str = "general",
    version: str = "1.0.0",
    dependencies: Optional[List[str]] = None,
):
    """Decorator to register a node class."""

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
        }

        # Register immediately if registry is available
        try:
            node_registry.register_node(
                name=node_name,
                node_class=cls,
                description=description,
                category=category,
                version=version,
                dependencies=dependencies,
            )
        except Exception as e:
            logger.warning(f"Failed to register node {node_name}: {e}")

        return cls

    return decorator
