from enum import Enum
from langchain_community.tools import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from quivr_core.llm_tools.entity import ToolsCategory


class WebSearchToolsList(str, Enum):
    TAVILY = "tavily"


WebSearchTools = ToolsCategory(
    name="WebSearch",
    description="Tools for web searching",
    tools=[WebSearchToolsList.TAVILY],
    default_tool=WebSearchToolsList.TAVILY,
)


def create_web_search_tool(tool_name: str, config: dict):
    if tool_name == WebSearchToolsList.TAVILY:
        required_keys = ["api_key"]
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required config key: {key}")
        tavily_api_wrapper = TavilySearchAPIWrapper(
            tavily_api_key=config["api_key"],
        )
        return TavilySearchResults(
            api_wrapper=tavily_api_wrapper,
            max_results=config.get("max_results", 5),
            search_depth=config.get("search_depth", "advanced"),
            include_answer=config.get("include_answer", True),
        )
    else:
        raise ValueError(f"Web search tool {tool_name} is not supported.")
