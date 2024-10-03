from enum import Enum
from typing import Dict, Any, Type, Union
from langchain_core.tools import BaseTool

from quivr_core.models import cited_answer
from quivr_core.llm_tools.web_search_tools import (
    create_web_search_tool,
    WebSearchToolsList,
)


class OtherToolsList(str, Enum):
    CITED_ANSWER = "cited_answer"


class LLMToolFactory:
    @staticmethod
    def create_tool(tool_name: str, config: Dict[str, Any]) -> Union[BaseTool, Type]:
        if tool_name in WebSearchToolsList.__members__.values():
            return create_web_search_tool(tool_name, config)
        elif tool_name == OtherToolsList.CITED_ANSWER:
            return cited_answer
        else:
            raise ValueError(f"Tool {tool_name} is not supported.")
