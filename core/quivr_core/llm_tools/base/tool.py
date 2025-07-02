"""
Base tool system for LLM tools with unified interface and lifecycle management.

This module provides abstract base classes for creating standardized tools
that can be registered, discovered, and executed consistently across the system.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, TypeVar, Generic, Type
from langchain_core.tools import BaseTool as LangChainBaseTool
from pydantic import BaseModel, Field

logger = logging.getLogger("quivr_core")

T = TypeVar("T", bound=BaseModel)


class ToolConfig(BaseModel):
    """Base configuration for tools."""

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

    Required class attributes that must be overridden in subclasses:
    - TOOL_NAME: str - Unique identifier for the tool
    - TOOL_TYPE: str - Category/type of the tool (e.g., 'search', 'processing')
    - TOOL_DESCRIPTION: str - Human-readable description of what the tool does
    - ARGS_SCHEMA: Type[BaseModel] - Pydantic model defining the tool's input schema

    Optional class attributes:
    - RUNTIME_ARGS_SCHEMA: Type[BaseModel] - Pydantic model defining runtime arguments needed during initialization
    """

    TOOL_NAME: str
    TOOL_DESCRIPTION: str
    TOOL_TYPE: str
    ARGS_SCHEMA: Type[BaseModel]
    RUNTIME_ARGS_SCHEMA: Optional[Type[BaseModel]] = None  # New optional attribute
    _tool_metadata: Optional[Dict[str, Any]] = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        required_attrs = {
            "TOOL_NAME": str,
            "TOOL_TYPE": str,
            "TOOL_DESCRIPTION": str,
            "ARGS_SCHEMA": type,
        }

        optional_attrs = {
            "RUNTIME_ARGS_SCHEMA": type,
        }

        # Validate required attributes
        for attr_name, attr_type in required_attrs.items():
            if not hasattr(cls, attr_name):
                raise TypeError(
                    f"Class {cls.__name__} must define class attribute '{attr_name}'"
                )

            attr_value = getattr(cls, attr_name)

            # Special validation for schema classes
            if attr_name in ["ARGS_SCHEMA"]:
                if not (
                    isinstance(attr_value, type) and issubclass(attr_value, BaseModel)
                ):
                    raise TypeError(
                        f"Class {cls.__name__}.{attr_name} must be a Pydantic BaseModel subclass, "
                        f"got {type(attr_value).__name__}"
                    )
            else:
                # Standard type checking for other attributes
                if not isinstance(attr_value, attr_type):
                    raise TypeError(
                        f"Class {cls.__name__}.{attr_name} must be of type {attr_type.__name__}, "
                        f"got {type(attr_value).__name__}"
                    )

                # Validate that string attributes are not empty or just whitespace
                if isinstance(attr_value, str):
                    if not attr_value.strip():
                        raise ValueError(
                            f"Class {cls.__name__}.{attr_name} cannot be empty or contain only whitespace"
                        )

                    # Optional: Validate minimum length for meaningful names/descriptions
                    if (
                        attr_name in ["TOOL_NAME", "TOOL_TYPE"]
                        and len(attr_value.strip()) < 2
                    ):
                        raise ValueError(
                            f"Class {cls.__name__}.{attr_name} must be at least 2 characters long"
                        )

                    if attr_name == "TOOL_DESCRIPTION" and len(attr_value.strip()) < 10:
                        raise ValueError(
                            f"Class {cls.__name__}.{attr_name} must be at least 10 characters long for meaningful description"
                        )

        # Validate optional attributes if they exist
        for attr_name, attr_type in optional_attrs.items():
            if hasattr(cls, attr_name):
                attr_value = getattr(cls, attr_name)
                if attr_value is not None:  # Only validate if not None
                    if attr_name == "RUNTIME_ARGS_SCHEMA":
                        if not (
                            isinstance(attr_value, type)
                            and issubclass(attr_value, BaseModel)
                        ):
                            raise TypeError(
                                f"Class {cls.__name__}.{attr_name} must be a Pydantic BaseModel subclass or None, "
                                f"got {type(attr_value).__name__}"
                            )

    def __init__(
        self,
        config: Optional[TConfig] = None,
        runtime_args: Optional[Dict[str, Any]] = None,
    ):
        """Initialize the base tool."""
        self.config: TConfig = config or ToolConfig()  # type: ignore
        self.logger = logging.getLogger(f"quivr_core.tools.{self.name}")

        # Validate and store runtime arguments
        self._runtime_args = self._validate_and_store_runtime_args(runtime_args)

        # Validate configuration
        self.validate_config()

    def _validate_and_store_runtime_args(
        self, runtime_args: Optional[Dict[str, Any]]
    ) -> Optional[BaseModel]:
        """Validate runtime arguments against the schema and return validated instance."""
        if self.RUNTIME_ARGS_SCHEMA is None:
            # Tool doesn't require runtime args
            if runtime_args:
                self.logger.warning(
                    f"Tool {self.name} doesn't accept runtime arguments, but some were provided"
                )
            return None

        if runtime_args is None:
            raise ValueError(
                f"Tool {self.name} requires runtime arguments as defined by {self.RUNTIME_ARGS_SCHEMA.__name__}"
            )

        try:
            # Validate runtime args against schema
            validated_args = self.RUNTIME_ARGS_SCHEMA.model_validate(runtime_args)
            return validated_args
        except Exception as e:
            raise ValueError(
                f"Runtime arguments validation failed for tool {self.name}: {e}"
            )

    @property
    def runtime_args_schema(self) -> Optional[Type[BaseModel]]:
        """Get the runtime arguments schema for this tool."""
        return self.RUNTIME_ARGS_SCHEMA

    @property
    def runtime_args(self) -> Optional[BaseModel]:
        """Get the validated runtime arguments instance."""
        return self._runtime_args

    def get_runtime_arg(self, name: str, default: Any = None) -> Any:
        """Get a specific runtime argument value."""
        if self._runtime_args is None:
            return default
        return getattr(self._runtime_args, name, default)

    def has_runtime_args(self) -> bool:
        """Check if tool has runtime arguments defined."""
        return self.RUNTIME_ARGS_SCHEMA is not None

    @property
    def name(self) -> str:
        """Get the tool name."""
        return self.TOOL_NAME

    @property
    def description(self) -> str:
        """Get the tool description."""
        return self.TOOL_DESCRIPTION

    @property
    def type(self) -> str:
        """Get the tool type."""
        return self.TOOL_TYPE

    @property
    def args_schema(self) -> Type[BaseModel]:
        """Get the input schema for this tool."""
        return self.ARGS_SCHEMA

    def validate_config(self) -> None:
        """Validate tool configuration. Override for specific validation."""
        pass

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
        error_msg = f"Error in {self.name}: {str(error)}"
        self.logger.error(error_msg, exc_info=True)

        return ToolResult(
            success=False,
            data=None,
            error=error_msg,
            execution_time=None,
            metadata={
                "tool_name": self.name,
                "input_data": str(input_data),
                "error_type": type(error).__name__,
            },
        )

    async def __call__(self, input_data: Any, **kwargs) -> ToolResult:
        """Main execution interface with full lifecycle management."""
        import time

        start_time = time.time()

        try:
            self.logger.debug(f"Executing {self.name}")

            # Validate and format input
            self.validate_input(input_data)
            formatted_input = self.format_input(input_data)

            # Execute the tool
            raw_result = await self.execute(formatted_input, **kwargs)

            # Format and validate output
            formatted_result = self.format_output(raw_result)
            self.validate_output(formatted_result)

            execution_time = time.time() - start_time
            self.logger.debug(f"Completed {self.name} in {execution_time:.2f}s")

            return ToolResult(
                success=True,
                data=formatted_result,
                execution_time=execution_time,
                metadata={"tool_name": self.name},
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

        async def tool_func(**kwargs) -> str:
            # Input will always be structured since ARGS_SCHEMA is mandatory
            result = await self(kwargs)

            if result.success:
                return str(result.data)
            else:
                raise Exception(result.error)

        return StructuredTool.from_function(
            func=tool_func,
            name=self.name,
            description=self.description,
            coroutine=tool_func,
            args_schema=self.args_schema,
        )

    def get_metadata(self) -> Dict[str, Any]:
        """Get tool metadata for registry."""
        return {
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "config": self.config.dict(),
            "class": self.__class__.__name__,
        }
