"""
Enhanced tool registry using the unified registry base and new BaseTool system.

This replaces the old entity.py approach with a clean, unified system that
follows the same patterns as prompts and nodes.
"""

from typing import Dict, Any, Callable, Union, Optional, List, Type
from langchain_core.tools import BaseTool as LangChainBaseTool
import logging

from quivr_core.registry_base import (
    BaseRegistry,
    BaseMetadata,
    create_registry_decorator,
)
from quivr_core.llm_tools.base.tool import QuivrBaseTool, ToolConfig

logger = logging.getLogger("quivr_core")


class ToolMetadata(BaseMetadata):
    """Metadata for a registered tool."""

    def __init__(
        self,
        tool_class_or_factory: Union[
            Type[QuivrBaseTool],
            Callable[[Dict[str, Any]], Union[QuivrBaseTool, LangChainBaseTool]],
        ],
        name: str,
        tool_type: str = "generic",
        config_schema: Optional[Type[ToolConfig]] = None,
        **kwargs,
    ):
        super().__init__(name=name, **kwargs)
        self.tool_class_or_factory = tool_class_or_factory
        self.tool_type = tool_type
        self.config_schema = config_schema or ToolConfig


class ToolRegistry(BaseRegistry[Union[Type[QuivrBaseTool], Callable], ToolMetadata]):
    """Registry for tool classes and factory functions."""

    def _create_metadata(
        self,
        name: str,
        item: Union[
            Type[QuivrBaseTool],
            Callable[[Dict[str, Any]], Union[QuivrBaseTool, LangChainBaseTool]],
        ],
        tool_type: str = "generic",
        config_schema: Optional[Type[ToolConfig]] = None,
        **kwargs,
    ) -> ToolMetadata:
        """Create metadata for a tool."""
        return ToolMetadata(
            tool_class_or_factory=item,
            name=name,
            tool_type=tool_type,
            config_schema=config_schema,
            **kwargs,
        )

    def _extract_item(
        self, metadata: ToolMetadata
    ) -> Union[Type[QuivrBaseTool], Callable]:
        """Extract the tool class or factory from metadata."""
        return metadata.tool_class_or_factory

    def _wrap_langchain_tool(
        self, langchain_tool: LangChainBaseTool, tool_name: str, metadata: ToolMetadata
    ) -> QuivrBaseTool:
        """Wrap a LangChain tool in our BaseTool interface."""

        class LangChainToolWrapper(QuivrBaseTool):
            TOOL_NAME = tool_name
            TOOL_TYPE = metadata.tool_type

            def __init__(
                self, lc_tool: LangChainBaseTool, config: Optional[ToolConfig] = None
            ):
                super().__init__(config=config)
                self.lc_tool = lc_tool

            async def execute(self, input_data: Any, **kwargs) -> Any:
                if hasattr(self.lc_tool, "arun"):
                    return await self.lc_tool.arun(input_data)
                else:
                    return self.lc_tool.run(input_data)

        tool_config = ToolConfig()
        return LangChainToolWrapper(langchain_tool, tool_config)

    def list_tools_by_type(self, tool_type: str) -> List[str]:
        """List tools filtered by tool type."""
        return [
            name
            for name, metadata in self._items.items()
            if metadata.tool_type == tool_type
        ]

    def get_tool_types(self) -> List[str]:
        """Get all available tool types."""
        return list(set(metadata.tool_type for metadata in self._items.values()))

    # Legacy compatibility methods
    def register_tool(
        self,
        tool_name: str,
        tool_class_or_factory: Union[Type[QuivrBaseTool], Callable],
        **kwargs,
    ) -> None:
        """Legacy method name for tool registration."""
        self.register(tool_name, tool_class_or_factory, **kwargs)


# Global registry instances
tool_registry = ToolRegistry()

# Decorators for easy registration
register_tool = create_registry_decorator(tool_registry)


def enhanced_register_tool(
    name: Optional[str] = None,
    description: str = "",
    category: str = "general",
    tool_type: str = "generic",
    config_schema: Optional[Type[ToolConfig]] = None,
    version: str = "1.0.0",
    tags: Optional[List[str]] = None,
):
    """Enhanced decorator with tool-specific options."""

    def decorator(
        tool_class_or_factory: Union[Type[QuivrBaseTool], Callable],
    ) -> Union[Type[QuivrBaseTool], Callable]:
        # Auto-detect tool name from TOOL_NAME attribute, fallback to class name
        tool_name = (
            name
            or getattr(tool_class_or_factory, "TOOL_NAME", None)
            or getattr(tool_class_or_factory, "__name__", "unnamed_tool")
        )

        # Auto-detect description from TOOL_DESCRIPTION attribute
        tool_description = description or getattr(
            tool_class_or_factory, "TOOL_DESCRIPTION", ""
        )

        # Auto-detect tool type from class if it's a BaseTool subclass
        if isinstance(tool_class_or_factory, type) and issubclass(
            tool_class_or_factory, QuivrBaseTool
        ):
            detected_type = getattr(tool_class_or_factory, "TOOL_TYPE", tool_type)
            actual_tool_type = (
                detected_type if detected_type != "generic" else tool_type
            )
        else:
            actual_tool_type = tool_type

        try:
            tool_registry.register(
                name=tool_name,
                item=tool_class_or_factory,
                description=tool_description,
                category=category,
                tool_type=actual_tool_type,
                config_schema=config_schema,
                version=version,
                tags=tags,
            )
        except Exception as e:
            logger.warning(f"Failed to register tool {tool_name}: {e}")

        return tool_class_or_factory

    return decorator


def list_available_tools(
    category: Optional[str] = None, tool_type: Optional[str] = None
) -> List[str]:
    """List all available tools, optionally filtered."""
    if tool_type:
        return tool_registry.list_tools_by_type(tool_type)
    return tool_registry.list_items(category=category)


def search_tools(query: str, categories: Optional[List[str]] = None) -> List[str]:
    """Search for tools by name or description."""
    return tool_registry.search(query, categories)
