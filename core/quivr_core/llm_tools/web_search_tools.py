from enum import Enum
from typing import Dict, List, Any
from langchain_community.tools import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from quivr_core.llm_tools.entity import ToolsCategory
import os
from pydantic import SecretStr  # Ensure correct import
from quivr_core.llm_tools.entity import ToolWrapper, ToolRegistry
from langchain_core.documents import Document


class WebSearchToolsList(str, Enum):
    TAVILY = "tavily"


def create_tavily_tool(config: Dict[str, Any]) -> ToolWrapper:
    api_key = (
        config.pop("api_key") if "api_key" in config else os.getenv("TAVILY_API_KEY")
    )
    if not api_key:
        raise ValueError(
            "Missing required config key 'api_key' or environment variable 'TAVILY_API_KEY'"
        )

    tavily_api_wrapper = TavilySearchAPIWrapper(
        tavily_api_key=SecretStr(api_key),
    )
    tool = TavilySearchResults(
        api_wrapper=tavily_api_wrapper,
        max_results=config.pop("max_results", 5),
        search_depth=config.pop("search_depth", "advanced"),
        include_answer=config.pop("include_answer", True),
        **config,
    )

    tool.name = WebSearchToolsList.TAVILY.value

    def format_input(task: str) -> Dict[str, Any]:
        return {"query": task}

    def format_output(response: Any) -> List[Document]:
        metadata = {"integration": "", "integration_link": ""}
        return [
            Document(
                page_content=d["content"],
                metadata={
                    **metadata,
                    "file_name": d["url"] if "url" in d else "",
                    "original_file_name": d["url"] if "url" in d else "",
                },
            )
            for d in response
        ]

    return ToolWrapper(tool, format_input, format_output)


# Initialize the registry and register tools
web_search_tool_registry = ToolRegistry()
web_search_tool_registry.register_tool(WebSearchToolsList.TAVILY, create_tavily_tool)


def create_web_search_tool(tool_name: str, config: Dict[str, Any]) -> ToolWrapper:
    return web_search_tool_registry.create_tool(tool_name, config)


WebSearchTools = ToolsCategory(
    name="Web Search",
    description="Tools for web searching",
    tools=[WebSearchToolsList.TAVILY],
    default_tool=WebSearchToolsList.TAVILY,
    create_tool=create_web_search_tool,
)
