"""
Prompt registry and management system for Quivr Core.

This module provides a centralized registry for managing prompt templates,
similar to the node registry system. It allows modules to register prompts
with metadata and provides discovery and retrieval capabilities.
"""

from .registry import (
    PromptMetadata,
    PromptRegistry,
    prompt_registry,
    register_prompt,
    get_prompt,
    list_available_prompts,
    search_prompts,
)

# Import all prompt modules to register them
# These imports are necessary for their side effects (registering prompts)
from .prompts import transform  # noqa: F401
from .prompts import classify  # noqa: F401
from .prompts import generate  # noqa: F401
from .prompts import system  # noqa: F401
from .prompts import document  # noqa: F401

__all__ = [
    "PromptMetadata",
    "PromptRegistry",
    "prompt_registry",
    "register_prompt",
    "get_prompt",
    "list_available_prompts",
    "search_prompts",
]
