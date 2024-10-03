from enum import Enum
from typing import Dict, Any
from langchain_core.tools import BaseTool
from langchain_community.tools import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from quivr_core.llm_tools.entity import ToolsCategory
import os
from pydantic.v1 import SecretStr as SecretStrV1  # Ensure correct import


class WebSearchToolsList(str, Enum):
    TAVILY = "tavily"


WebSearchTools = ToolsCategory(
    name="WebSearch",
    description="Tools for web searching",
    tools=[WebSearchToolsList.TAVILY],
    default_tool=WebSearchToolsList.TAVILY,
)


def create_web_search_tool(tool_name: str, config: Dict[str, Any]) -> BaseTool:
    if tool_name == WebSearchToolsList.TAVILY:
        api_key = config.pop("api_key") or os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError(
                f"Missing required config key 'api_key' or environment variable "
                f"'TAVILY_API_KEY' for the tool {tool_name}"
            )

        tavily_api_wrapper = TavilySearchAPIWrapper(
            tavily_api_key=SecretStrV1(api_key),  # Use the correct SecretStr
        )
        return TavilySearchResults(
            api_wrapper=tavily_api_wrapper,
            max_results=config.pop("max_results", 5),
            search_depth=config.pop("search_depth", "advanced"),
            include_answer=config.pop("include_answer", True),
            **config,  # Pass any additional keyword arguments
        )
    else:
        raise ValueError(f"Web search tool {tool_name} is not supported.")
