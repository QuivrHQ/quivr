"""
Enhanced prompt registry using the unified registry base.

This demonstrates how the existing PromptRegistry can be refactored
to use the new base registry system while maintaining all functionality.
"""

from typing import Union, Callable, Optional
from langchain_core.prompts.base import BasePromptTemplate

from quivr_core.registry_base import (
    BaseRegistry,
    BaseMetadata,
    create_registry_decorator,
)


class PromptMetadata(BaseMetadata):
    """Metadata for a registered prompt."""

    def __init__(self, prompt_template: BasePromptTemplate, name: str, **kwargs):
        super().__init__(name=name, **kwargs)
        self.prompt_template = prompt_template


class PromptRegistry(BaseRegistry[BasePromptTemplate, PromptMetadata]):
    """Registry for discovering and managing prompt templates."""

    def _create_metadata(
        self,
        name: str,
        item: Union[BasePromptTemplate, Callable[[], BasePromptTemplate]],
        **kwargs,
    ) -> PromptMetadata:
        """Create metadata for a prompt template."""
        # Handle both direct templates and factory functions
        if callable(item) and not isinstance(item, BasePromptTemplate):
            try:
                prompt_template = item()
            except Exception as e:
                raise ValueError(
                    f"Failed to create prompt from function {getattr(item, '__name__', 'unknown')}: {e}"
                )
        else:
            prompt_template = item

        return PromptMetadata(prompt_template=prompt_template, name=name, **kwargs)

    def _extract_item(self, metadata: PromptMetadata) -> BasePromptTemplate:
        """Extract the prompt template from metadata."""
        return metadata.prompt_template

    # Legacy method names for backward compatibility
    def register_prompt(
        self, name: str, prompt_template: BasePromptTemplate, **kwargs
    ) -> None:
        """Legacy method name for prompt registration."""
        self.register(name, prompt_template, **kwargs)

    def get_prompt(self, name: str) -> BasePromptTemplate:
        """Legacy method name for getting prompts."""
        return self.get(name)

    def get_prompt_metadata(self, name: str) -> PromptMetadata:
        """Legacy method name for getting prompt metadata."""
        return self.get_metadata(name)

    def list_prompts(
        self, category: Optional[str] = None, tag: Optional[str] = None
    ) -> list[str]:
        """Legacy method name for listing prompts."""
        return self.list_items(category=category, tag=tag)

    def search_prompts(
        self, query: str, categories: Optional[list[str]] = None
    ) -> list[str]:
        """Legacy method name for searching prompts."""
        return self.search(query, categories)

    def has_prompt(self, name: str) -> bool:
        """Legacy method name for checking prompt existence."""
        return self.has_item(name)

    def unregister_prompt(self, name: str) -> None:
        """Legacy method name for unregistering prompts."""
        self.unregister(name)


# Global registry instance
prompt_registry = PromptRegistry()

# Decorator for easy prompt registration
register_prompt = create_registry_decorator(prompt_registry)


# Convenience functions
def get_prompt(name: str) -> BasePromptTemplate:
    """Get a prompt by name from the registry."""
    return prompt_registry.get(name)


def list_available_prompts(category: Optional[str] = None) -> list[str]:
    """List all available prompts, optionally filtered by category."""
    return prompt_registry.list_items(category=category)


def search_prompts(query: str, categories: Optional[list[str]] = None) -> list[str]:
    """Search for prompts by name or description."""
    return prompt_registry.search(query, categories)
