"""
Base registry system for managing and discovering registered components.

This module provides abstract base classes for creating specialized registries
across the Quivr Core system, ensuring consistent patterns for registration,
discovery, and metadata management.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, TypeVar, Generic, Callable
import logging

logger = logging.getLogger("quivr_core")

T = TypeVar(
    "T"
)  # The type being registered (e.g., BasePromptTemplate, Type[BaseNode], etc.)
M = TypeVar("M", bound="BaseMetadata")  # The metadata type


class BaseMetadata(ABC):
    """Base metadata class for all registry entries."""

    def __init__(
        self,
        name: str,
        description: str = "",
        category: str = "general",
        version: str = "1.0.0",
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ):
        self.name = name
        self.description = description
        self.category = category
        self.version = version
        self.tags = tags or []
        # Store any additional metadata
        for key, value in kwargs.items():
            setattr(self, key, value)


class BaseRegistry(Generic[T, M], ABC):
    """Base registry class for managing registered components."""

    def __init__(self):
        self._items: Dict[str, M] = {}
        self._categories: Dict[str, List[str]] = {}
        self._tags: Dict[str, List[str]] = {}

    @abstractmethod
    def _create_metadata(self, name: str, item: T, **kwargs: Any) -> M:
        """Create metadata for a registered item."""
        pass

    @abstractmethod
    def _extract_item(self, metadata: M) -> T:
        """Extract the registered item from metadata."""
        pass

    def register(
        self,
        name: str,
        item: T,
        description: str = "",
        category: str = "general",
        version: str = "1.0.0",
        tags: Optional[List[str]] = None,
        **kwargs,
    ) -> None:
        """Register an item with metadata."""

        if name in self._items:
            logger.warning(f"Overriding existing registration: {name}")

        metadata = self._create_metadata(
            name=name,
            item=item,
            description=description,
            category=category,
            version=version,
            tags=tags,
            **kwargs,
        )

        self._items[name] = metadata
        self._update_indices(name, metadata)

        logger.info(
            f"Registered {self.__class__.__name__} item: {name} (category: {category})"
        )

    def _update_indices(self, name: str, metadata: M) -> None:
        """Update category and tag indices."""
        # Update category index
        if metadata.category not in self._categories:
            self._categories[metadata.category] = []
        if name not in self._categories[metadata.category]:
            self._categories[metadata.category].append(name)

        # Update tag index
        for tag in metadata.tags:
            if tag not in self._tags:
                self._tags[tag] = []
            if name not in self._tags[tag]:
                self._tags[tag].append(name)

    def get(self, name: str) -> T:
        """Get a registered item by name."""
        if name not in self._items:
            raise KeyError(f"Item '{name}' not found in registry")
        return self._extract_item(self._items[name])

    def get_metadata(self, name: str) -> M:
        """Get metadata for a registered item."""
        if name not in self._items:
            raise KeyError(f"Item '{name}' not found in registry")
        return self._items[name]

    def list_items(
        self, category: Optional[str] = None, tag: Optional[str] = None
    ) -> List[str]:
        """List all registered item names, optionally filtered."""
        if category:
            return self._categories.get(category, [])
        if tag:
            return self._tags.get(tag, [])
        return list(self._items.keys())

    def list_categories(self) -> List[str]:
        """List all available categories."""
        return list(self._categories.keys())

    def list_tags(self) -> List[str]:
        """List all available tags."""
        return list(self._tags.keys())

    def search(self, query: str, categories: Optional[List[str]] = None) -> List[str]:
        """Search items by name or description."""
        results = []
        query_lower = query.lower()

        for name, metadata in self._items.items():
            if categories and metadata.category not in categories:
                continue

            if (
                query_lower in name.lower()
                or query_lower in metadata.description.lower()
            ):
                results.append(name)

        return results

    def has_item(self, name: str) -> bool:
        """Check if an item is registered."""
        return name in self._items

    def unregister(self, name: str) -> None:
        """Unregister an item."""
        if name not in self._items:
            raise KeyError(f"Item '{name}' not found in registry")

        metadata = self._items[name]

        # Remove from category index
        if metadata.category in self._categories:
            if name in self._categories[metadata.category]:
                self._categories[metadata.category].remove(name)
            if not self._categories[metadata.category]:
                del self._categories[metadata.category]

        # Remove from tag index
        for tag in metadata.tags:
            if tag in self._tags and name in self._tags[tag]:
                self._tags[tag].remove(name)
                if not self._tags[tag]:
                    del self._tags[tag]

        del self._items[name]
        logger.info(f"Unregistered item: {name}")


def create_registry_decorator(registry_instance: BaseRegistry) -> Callable:
    """Create a decorator for easy registration with a registry."""

    def decorator(
        name: Optional[str] = None,
        description: str = "",
        category: str = "general",
        version: str = "1.0.0",
        tags: Optional[List[str]] = None,
        **kwargs,
    ):
        def inner_decorator(item_or_func):
            # Handle both direct items and factory functions
            if callable(item_or_func) and not hasattr(item_or_func, "__name__"):
                # Direct item (like a prompt template)
                item_name = name or str(item_or_func)
                actual_item = item_or_func
            else:
                # Function or class
                item_name = name or getattr(item_or_func, "__name__", "unnamed_item")
                actual_item = item_or_func

            try:
                registry_instance.register(
                    name=item_name,
                    item=actual_item,
                    description=description,
                    category=category,
                    version=version,
                    tags=tags,
                    **kwargs,
                )
            except Exception as e:
                logger.warning(f"Failed to register {item_name}: {e}")

            return item_or_func

        return inner_decorator

    return decorator
