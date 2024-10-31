from quivr_core.base_config import QuivrBaseConfig
from typing import Callable
from langchain_core.tools import BaseTool
from typing import Dict, Any


class ToolsCategory(QuivrBaseConfig):
    name: str
    description: str
    tools: list
    default_tool: str | None = None
    create_tool: Callable

    def __init__(self, **data):
        super().__init__(**data)
        self.name = self.name.lower()


class ToolWrapper:
    def __init__(self, tool: BaseTool, format_input: Callable, format_output: Callable):
        self.tool = tool
        self.format_input = format_input
        self.format_output = format_output


class ToolRegistry:
    def __init__(self):
        self._registry = {}

    def register_tool(self, tool_name: str, create_func: Callable):
        self._registry[tool_name] = create_func

    def create_tool(self, tool_name: str, config: Dict[str, Any]) -> ToolWrapper:
        if tool_name not in self._registry:
            raise ValueError(f"Tool {tool_name} is not supported.")
        return self._registry[tool_name](config)
