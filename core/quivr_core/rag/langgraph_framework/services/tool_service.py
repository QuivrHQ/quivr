import logging
from typing import Any, Dict, List, Optional, Type
from langchain_core.tools import BaseTool as LangChainBaseTool
from pydantic import BaseModel

from quivr_core.rag.entities.tools import ToolsConfig
from quivr_core.llm_tools.registry import tool_registry
from quivr_core.llm_tools.base.tool import QuivrBaseTool

logger = logging.getLogger("quivr_core")


class ToolCallTracker:
    """Tracks tool calls, their inputs, outputs, and counts."""

    def __init__(self, max_tool_calls: Optional[int] = None):
        self.max_tool_calls = max_tool_calls
        self.tool_calls: List[Dict[str, Any]] = []
        self.call_count = 0

    def can_make_call(self) -> bool:
        """Check if we can make another tool call."""
        if self.max_tool_calls is None:
            return True
        return self.call_count < self.max_tool_calls

    def track_call(
        self,
        tool_name: str,
        input_data: Any,
        output_data: Any,
        success: bool = True,
        error: Optional[str] = None,
    ):
        """Track a tool call."""
        self.call_count += 1
        self.tool_calls.append(
            {
                "tool_name": tool_name,
                "input": input_data,
                "output": output_data,
                "success": success,
                "error": error,
                "call_number": self.call_count,
            }
        )

    def get_calls_summary(self) -> Dict[str, Any]:
        """Get summary of all tool calls."""
        return {
            "total_calls": self.call_count,
            "max_calls": self.max_tool_calls,
            "calls": self.tool_calls,
        }


class ToolService:
    """Service for tool management and execution."""

    def __init__(
        self, config: ToolsConfig, runtime_context: Optional[Dict[str, Any]] = None
    ):
        self.config = config
        self.runtime_context = runtime_context or {}
        self.logger = logger
        self._tool_cache: Dict[str, QuivrBaseTool] = {}

    def extract_tools_from_config(self) -> List[QuivrBaseTool]:
        """Extract and instantiate tools from config using runtime context."""
        tools: List[QuivrBaseTool] = []

        if not self.config.tools:
            return tools

        for tool_config in self.config.tools:
            tool_name = tool_config.name
            if not tool_name:
                self.logger.warning("Tool config missing 'name' field")
                continue

            try:
                # Get tool from registry
                if not tool_registry.has_item(tool_name):
                    self.logger.error(f"Tool '{tool_name}' not found in registry")
                    raise ValueError(f"Tool '{tool_name}' not found in registry")

                # Create cache key including runtime context
                cache_key = f"{tool_name}_{hash(str(tool_config.config) if tool_config.config else 'default')}_{hash(str(self.runtime_context))}"
                if cache_key in self._tool_cache:
                    tools.append(self._tool_cache[cache_key])
                    continue

                # Get tool class from registry
                tool_metadata = tool_registry.get_metadata(tool_name)
                tool_class_or_factory = tool_metadata.tool_class_or_factory

                # Check if tool requires runtime args and extract from runtime context
                tool_runtime_args = None
                if isinstance(tool_class_or_factory, type) and issubclass(
                    tool_class_or_factory, QuivrBaseTool
                ):
                    # Check if tool has RUNTIME_ARGS_SCHEMA
                    if (
                        hasattr(tool_class_or_factory, "RUNTIME_ARGS_SCHEMA")
                        and tool_class_or_factory.RUNTIME_ARGS_SCHEMA is not None
                    ):
                        # Extract runtime args from the runtime context based on what the tool needs
                        tool_runtime_args = self._extract_runtime_args_for_tool(
                            tool_class_or_factory, tool_name
                        )

                    # Instantiate tool with runtime arguments
                    tool_instance = tool_class_or_factory(
                        config=tool_config, runtime_args=tool_runtime_args
                    )
                elif callable(tool_class_or_factory):
                    # For factory functions, we still pass the extracted runtime args
                    tool_runtime_args = self._extract_runtime_args_for_factory(
                        tool_name
                    )
                    tool_instance = tool_class_or_factory(
                        tool_config, tool_runtime_args
                    )

                    # If factory returns a LangChain tool, wrap it
                    if isinstance(tool_instance, LangChainBaseTool) and not isinstance(
                        tool_instance, QuivrBaseTool
                    ):
                        tool_instance = tool_registry._wrap_langchain_tool(
                            tool_instance, tool_name, tool_metadata
                        )
                else:
                    self.logger.error(f"Invalid tool type for '{tool_name}'")
                    raise ValueError(f"Invalid tool type for '{tool_name}'")

                # Cache and add to results
                self._tool_cache[cache_key] = tool_instance
                tools.append(tool_instance)

            except Exception as e:
                self.logger.error(f"Failed to instantiate tool '{tool_name}': {e}")
                raise e

        return tools

    def _extract_runtime_args_for_tool(
        self, tool_class: Type[QuivrBaseTool], tool_name: str
    ) -> Optional[Dict[str, Any]]:
        """Extract runtime arguments for a tool from the runtime context."""
        if (
            not hasattr(tool_class, "RUNTIME_ARGS_SCHEMA")
            or tool_class.RUNTIME_ARGS_SCHEMA is None
        ):
            return None

        runtime_schema = tool_class.RUNTIME_ARGS_SCHEMA
        runtime_args = {}

        # Get the fields from the schema and extract matching values from runtime context
        for field_name, field_info in runtime_schema.model_fields.items():
            if field_name in self.runtime_context:
                runtime_args[field_name] = self.runtime_context[field_name]
            elif not field_info.is_required():
                # Optional field, skip if not in context
                continue
            else:
                # Required field missing
                raise ValueError(
                    f"Tool '{tool_name}' requires runtime argument '{field_name}' but it's not available in runtime context"
                )

        return runtime_args if runtime_args else None

    def _extract_runtime_args_for_factory(
        self, tool_name: str
    ) -> Optional[Dict[str, Any]]:
        """Extract runtime arguments for factory functions. Override this method for specific factory tools."""
        # For factory functions, we can implement tool-specific logic here
        # or return the entire runtime context for backward compatibility
        return self.runtime_context if self.runtime_context else None

    def convert_to_langchain_tools(
        self, quivr_tools: List[QuivrBaseTool]
    ) -> List[LangChainBaseTool]:
        """Convert QuivrBaseTool instances to LangChain tools."""
        langchain_tools = []

        for tool in quivr_tools:
            try:
                lc_tool = tool.to_langchain_tool()
                langchain_tools.append(lc_tool)
            except Exception as e:
                self.logger.error(
                    f"Failed to convert tool '{tool.name}' to LangChain format: {e}"
                )
                raise e

        return langchain_tools

    def create_tool_tracker(self) -> ToolCallTracker:
        """Create a new tool call tracker."""
        return ToolCallTracker(max_tool_calls=self.config.max_tool_calls)

    async def execute_tool_by_name(
        self,
        tool_name: str,
        tool_input: Any,
        tools: List[QuivrBaseTool],
        tracker: ToolCallTracker,
    ) -> Dict[str, Any]:
        """Execute a specific tool by name and track the call."""
        if not tracker.can_make_call():
            self.logger.warning(
                f"Maximum tool calls ({tracker.max_tool_calls}) reached"
            )
            return {
                "success": False,
                "error": f"Maximum tool calls ({tracker.max_tool_calls}) reached",
            }

        # Find and execute the tool
        for tool in tools:
            if tool.name == tool_name:
                try:
                    result = await tool(tool_input)
                    tracker.track_call(
                        tool_name=tool_name,
                        input_data=tool_input,
                        output_data=result.data,
                        success=result.success,
                        error=result.error,
                    )
                    return {"success": True, "result": result, "tool_name": tool_name}
                except Exception as e:
                    error_msg = str(e)
                    tracker.track_call(
                        tool_name=tool_name,
                        input_data=tool_input,
                        output_data=None,
                        success=False,
                        error=error_msg,
                    )
                    return {
                        "success": False,
                        "error": error_msg,
                        "tool_name": tool_name,
                    }

        # Tool not found
        error_msg = f"Tool '{tool_name}' not found in available tools"
        self.logger.warning(error_msg)
        return {"success": False, "error": error_msg, "tool_name": tool_name}

    def prepare_tools_for_node(
        self,
    ) -> Dict[str, Any]:
        """Prepare tools for a node: extract from config and create tracker (no LLM binding)."""
        try:
            # Extract tools from config
            quivr_tools = self.extract_tools_from_config()

            # Convert to LangChain tools if any tools exist
            langchain_tools = []
            if quivr_tools:
                langchain_tools = self.convert_to_langchain_tools(quivr_tools)

            # Create tracker
            tracker = self.create_tool_tracker()

            self.logger.info(f"Prepared {len(quivr_tools)} tools")

            return {
                "quivr_tools": quivr_tools,
                "langchain_tools": langchain_tools,
                "tracker": tracker,
                "success": True,
            }

        except Exception as e:
            self.logger.error(f"Failed to prepare tools: {e}")
            return {
                "quivr_tools": [],
                "langchain_tools": [],
                "tracker": self.create_tool_tracker(),
                "success": False,
                "error": str(e),
            }

    def get_tool_by_name(
        self, tool_name: str, tools: List[QuivrBaseTool]
    ) -> Optional[QuivrBaseTool]:
        """Get a tool by name from a list of tools."""
        for tool in tools:
            if tool.name == tool_name:
                return tool
        return None

    def get_tools_runtime_requirements(self) -> Dict[str, Optional[Type[BaseModel]]]:
        """Get runtime argument requirements for all tools in config."""
        requirements: Dict[str, Optional[Type[BaseModel]]] = {}

        if not self.config.tools:
            return requirements

        for tool_config in self.config.tools:
            tool_name = tool_config.name
            if not tool_name:
                continue

            if tool_registry.has_item(tool_name):
                tool_metadata = tool_registry.get_metadata(tool_name)
                tool_class = tool_metadata.tool_class_or_factory

                if isinstance(tool_class, type) and issubclass(
                    tool_class, QuivrBaseTool
                ):
                    runtime_schema = getattr(tool_class, "RUNTIME_ARGS_SCHEMA", None)
                    requirements[tool_name] = runtime_schema

        return requirements
