"""
Prompt registry system for managing and discovering prompt templates.

This module provides a centralized registry for prompt templates, allowing
modules to register prompts with metadata and enabling discovery and retrieval
capabilities similar to the node registry system.
"""

from typing import Dict, List, Optional, Callable, TypeVar, Union
import logging

from langchain_core.prompts.base import BasePromptTemplate

# Type variable for the decorator
T = TypeVar("T", bound=Callable[[], BasePromptTemplate])

logger = logging.getLogger("quivr_core")


class PromptMetadata:
    """Metadata for a registered prompt."""

    def __init__(
        self,
        prompt_template: BasePromptTemplate,
        name: str,
        description: str = "",
        category: str = "general",
        version: str = "1.0.0",
        tags: Optional[List[str]] = None,
    ):
        self.prompt_template = prompt_template
        self.name = name
        self.description = description
        self.category = category
        self.version = version
        self.tags = tags or []


class PromptRegistry:
    """Registry for discovering and managing prompt templates."""

    def __init__(self):
        self._prompts: Dict[str, PromptMetadata] = {}
        self._categories: Dict[str, List[str]] = {}
        self._tags: Dict[str, List[str]] = {}

    def register_prompt(
        self,
        name: str,
        prompt_template: BasePromptTemplate,
        description: str = "",
        category: str = "general",
        version: str = "1.0.0",
        tags: Optional[List[str]] = None,
    ) -> None:
        """Register a prompt template."""

        if name in self._prompts:
            logger.warning(f"Overriding existing prompt registration: {name}")

        metadata = PromptMetadata(
            prompt_template=prompt_template,
            name=name,
            description=description,
            category=category,
            version=version,
            tags=tags,
        )

        self._prompts[name] = metadata

        # Update category index
        if category not in self._categories:
            self._categories[category] = []
        if name not in self._categories[category]:
            self._categories[category].append(name)

        # Update tag index
        for tag in tags or []:
            if tag not in self._tags:
                self._tags[tag] = []
            if name not in self._tags[tag]:
                self._tags[tag].append(name)

        logger.info(f"Registered prompt: {name} (category: {category})")

    def get_prompt(self, name: str) -> BasePromptTemplate:
        """Get a prompt template by name."""
        if name not in self._prompts:
            raise KeyError(f"Prompt '{name}' not found in registry")
        return self._prompts[name].prompt_template

    def get_prompt_metadata(self, name: str) -> PromptMetadata:
        """Get prompt metadata by name."""
        if name not in self._prompts:
            raise KeyError(f"Prompt '{name}' not found in registry")
        return self._prompts[name]

    def list_prompts(
        self, category: Optional[str] = None, tag: Optional[str] = None
    ) -> List[str]:
        """List all registered prompt names, optionally filtered by category or tag."""
        if category:
            return self._categories.get(category, [])
        if tag:
            return self._tags.get(tag, [])
        return list(self._prompts.keys())

    def list_categories(self) -> List[str]:
        """List all available categories."""
        return list(self._categories.keys())

    def list_tags(self) -> List[str]:
        """List all available tags."""
        return list(self._tags.keys())

    def search_prompts(
        self, query: str, categories: Optional[List[str]] = None
    ) -> List[str]:
        """Search prompts by name or description."""
        results = []
        query_lower = query.lower()

        for name, metadata in self._prompts.items():
            if categories and metadata.category not in categories:
                continue

            if (
                query_lower in name.lower()
                or query_lower in metadata.description.lower()
            ):
                results.append(name)

        return results

    def has_prompt(self, name: str) -> bool:
        """Check if a prompt is registered."""
        return name in self._prompts

    def unregister_prompt(self, name: str) -> None:
        """Unregister a prompt template."""
        if name not in self._prompts:
            raise KeyError(f"Prompt '{name}' not found in registry")

        metadata = self._prompts[name]

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

        del self._prompts[name]
        logger.info(f"Unregistered prompt: {name}")


# Global registry instance
prompt_registry = PromptRegistry()


# Decorator for easy prompt registration
def register_prompt(
    name: Optional[str] = None,
    description: str = "",
    category: str = "general",
    version: str = "1.0.0",
    tags: Optional[List[str]] = None,
):
    """Decorator to register a prompt template or prompt factory function."""

    def decorator(
        prompt_func_or_template: Union[T, BasePromptTemplate],
    ) -> Union[T, BasePromptTemplate]:
        # Handle both functions that return prompts and direct prompt templates
        if callable(prompt_func_or_template) and not isinstance(
            prompt_func_or_template, BasePromptTemplate
        ):
            # It's a function that returns a prompt
            prompt_func = prompt_func_or_template
            prompt_name = name or getattr(
                prompt_func, "__name__", "unnamed_prompt"
            ).replace("create_", "").replace("_prompt", "")

            # Call the function to get the actual prompt
            try:
                prompt_template = prompt_func()
            except Exception as e:
                logger.error(
                    f"Failed to create prompt from function {prompt_func.__name__}: {e}"
                )
                return prompt_func_or_template
        else:
            # It's a direct prompt template
            prompt_template = prompt_func_or_template
            prompt_name = name or getattr(prompt_template, "name", "unnamed_prompt")

        # Ensure prompt_name is always a string
        if not isinstance(prompt_name, str):
            prompt_name = str(prompt_name)

        # Register the prompt
        try:
            prompt_registry.register_prompt(
                name=prompt_name,
                prompt_template=prompt_template,
                description=description,
                category=category,
                version=version,
                tags=tags,
            )
        except Exception as e:
            logger.warning(f"Failed to register prompt {prompt_name}: {e}")

        return prompt_func_or_template

    return decorator


# Convenience functions for accessing prompts
def get_prompt(name: str) -> BasePromptTemplate:
    """Get a prompt by name from the registry."""
    return prompt_registry.get_prompt(name)


def list_available_prompts(category: Optional[str] = None) -> List[str]:
    """List all available prompts, optionally filtered by category."""
    return prompt_registry.list_prompts(category=category)


def search_prompts(query: str, categories: Optional[List[str]] = None) -> List[str]:
    """Search for prompts by name or description."""
    return prompt_registry.search_prompts(query, categories)
