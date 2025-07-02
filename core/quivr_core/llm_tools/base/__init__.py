"""
Base classes for LLM tools with unified interface and lifecycle management.
"""

from .tool import (
    QuivrBaseTool,
    ToolConfig,
    ToolResult,
)

__all__ = [
    "QuivrBaseTool",
    "ToolConfig",
    "ToolResult",
]
