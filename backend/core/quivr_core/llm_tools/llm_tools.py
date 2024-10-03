from typing import Dict, Any, Type, Union
from langchain_core.tools import BaseTool

from quivr_core.llm_tools.web_search_tools import (
    create_web_search_tool,
    WebSearchTools,
)

from quivr_core.llm_tools.other_tools import (
    create_other_tool,
    OtherTools,
)


class LLMToolFactory:
    @staticmethod
    def create_tool(tool_name: str, config: Dict[str, Any]) -> Union[BaseTool, Type]:
        if tool_name in WebSearchTools.tools:
            return create_web_search_tool(tool_name, config)
        elif tool_name in OtherTools.tools:
            return create_other_tool(tool_name, config)
        else:
            raise ValueError(f"Tool {tool_name} is not supported.")


TOOLS_CATEGORIES = {
    WebSearchTools.name: WebSearchTools,
    OtherTools.name: OtherTools,
}

# Register all ToolsList enums
TOOLS_LISTS = {
    **{tool.value: tool for tool in WebSearchTools.tools},
    **{tool.value: tool for tool in OtherTools.tools},
}
