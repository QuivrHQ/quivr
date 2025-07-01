"""
Base tool system for LLM tools with unified interface and lifecycle management.

This module provides abstract base classes for creating standardized tools
that can be registered, discovered, and executed consistently across the system.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar, Generic
from langchain_core.tools import BaseTool as LangChainBaseTool
from langchain_core.documents import Document
from pydantic import BaseModel, Field

logger = logging.getLogger("quivr_core")

T = TypeVar("T", bound=BaseModel)


class ToolConfig(BaseModel):
    """Base configuration for tools."""

    name: str = Field(..., description="Tool name")
    description: Optional[str] = Field(default=None, description="Tool description")
    max_retries: int = Field(
        default=3, description="Maximum number of retries on failure"
    )
    timeout: float = Field(default=60, description="Timeout in seconds")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )


# Generic type for tool config
TConfig = TypeVar("TConfig", bound=ToolConfig)


class ToolResult(BaseModel):
    """Standardized tool execution result."""

    success: bool = Field(..., description="Whether the tool execution succeeded")
    data: Any = Field(default=None, description="Tool output data")
    error: Optional[str] = Field(default=None, description="Error message if failed")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional result metadata"
    )
    execution_time: Optional[float] = Field(
        default=None, description="Execution time in seconds"
    )


class QuivrBaseTool(ABC, Generic[TConfig]):
    """
    Abstract base class for all LLM tools with standardized interface.

    This provides a consistent pattern similar to BaseNode for tool development,
    with proper lifecycle management, configuration, and error handling.
    """

    TOOL_NAME: str = "base_tool"
    TOOL_TYPE: str = "generic"
    _tool_metadata: Optional[Dict[str, Any]] = None

    def __init__(
        self,
        config: Optional[TConfig] = None,
        tool_name: Optional[str] = None,
    ):
        """Initialize the base tool."""
        self.tool_name = tool_name or self.TOOL_NAME
        self.config: TConfig = config or ToolConfig(name=self.tool_name)  # type: ignore
        self.logger = logging.getLogger(f"quivr_core.tools.{self.tool_name}")

        # Validate configuration
        self.validate_config()

    @property
    def name(self) -> str:
        """Get the tool name."""
        return self.tool_name

    @property
    def type(self) -> str:
        """Get the tool type."""
        return self.TOOL_TYPE

    def validate_config(self) -> None:
        """Validate tool configuration. Override for specific validation."""
        if not self.config.name:
            raise ValueError(f"Tool {self.__class__.__name__} must have a name")

    def validate_input(self, input_data: Any) -> None:
        """Validate input data. Override in subclasses for specific validation."""
        pass

    def validate_output(self, output_data: Any) -> None:
        """Validate output data. Override in subclasses for specific validation."""
        pass

    def format_input(self, raw_input: Any) -> Any:
        """Format raw input for tool execution. Override as needed."""
        return raw_input

    def format_output(self, raw_output: Any) -> Any:
        """Format raw output from tool execution. Override as needed."""
        return raw_output

    def handle_error(self, error: Exception, input_data: Any) -> ToolResult:
        """Handle errors during execution."""
        error_msg = f"Error in {self.tool_name}: {str(error)}"
        self.logger.error(error_msg, exc_info=True)

        return ToolResult(
            success=False,
            data=None,
            error=error_msg,
            execution_time=None,
            metadata={
                "tool_name": self.tool_name,
                "input_data": str(input_data),
                "error_type": type(error).__name__,
            },
        )

    async def __call__(self, input_data: Any, **kwargs) -> ToolResult:
        """Main execution interface with full lifecycle management."""
        import time

        start_time = time.time()

        try:
            self.logger.debug(f"Executing {self.tool_name}")

            # Validate and format input
            self.validate_input(input_data)
            formatted_input = self.format_input(input_data)

            # Execute the tool
            raw_result = await self.execute(formatted_input, **kwargs)

            # Format and validate output
            formatted_result = self.format_output(raw_result)
            self.validate_output(formatted_result)

            execution_time = time.time() - start_time
            self.logger.debug(f"Completed {self.tool_name} in {execution_time:.2f}s")

            return ToolResult(
                success=True,
                data=formatted_result,
                execution_time=execution_time,
                metadata={"tool_name": self.tool_name},
            )

        except Exception as e:
            return self.handle_error(e, input_data)

    @abstractmethod
    async def execute(self, input_data: Any, **kwargs) -> Any:
        """Execute the core tool logic. Must be implemented by subclasses."""
        pass

    def to_langchain_tool(self) -> LangChainBaseTool:
        """Convert to LangChain tool format for compatibility."""
        from langchain_core.tools import StructuredTool

        async def tool_func(input_data: str) -> str:
            result = await self(input_data)
            if result.success:
                return str(result.data)
            else:
                raise Exception(result.error)

        return StructuredTool.from_function(
            func=tool_func,
            name=self.tool_name,
            description=self.config.description,
            coroutine=tool_func,
        )

    def get_metadata(self) -> Dict[str, Any]:
        """Get tool metadata for registry."""
        return {
            "name": self.tool_name,
            "type": self.type,
            "description": self.config.description,
            "config": self.config.dict(),
            "class": self.__class__.__name__,
        }


class DocumentTool(QuivrBaseTool[TConfig]):
    """Base class for tools that return document-based results."""

    TOOL_TYPE = "document"

    def format_output(self, raw_output: Any) -> List[Document]:
        """Format output as Document objects."""
        if isinstance(raw_output, list) and all(
            isinstance(d, Document) for d in raw_output
        ):
            return raw_output
        elif isinstance(raw_output, Document):
            return [raw_output]
        elif isinstance(raw_output, str):
            return [Document(page_content=raw_output)]
        elif isinstance(raw_output, dict):
            content = raw_output.get("content", str(raw_output))
            metadata = raw_output.get("metadata", {})
            return [Document(page_content=content, metadata=metadata)]
        else:
            return [Document(page_content=str(raw_output))]


class SearchTool(DocumentTool[TConfig]):
    """Base class for search-based tools."""

    TOOL_TYPE = "search"

    def validate_input(self, input_data: Any) -> None:
        """Validate search input."""
        if not input_data:
            raise ValueError("Search query cannot be empty")
        if not isinstance(input_data, (str, dict)):
            raise ValueError("Search input must be string or dict")


class ProcessingTool(QuivrBaseTool[TConfig]):
    """Base class for data processing tools."""

    TOOL_TYPE = "processing"

    def format_input(self, raw_input: Any) -> Dict[str, Any]:
        """Format input as dictionary for processing."""
        if isinstance(raw_input, dict):
            return raw_input
        elif isinstance(raw_input, str):
            return {"content": raw_input}
        else:
            return {"data": raw_input}
