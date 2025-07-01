"""
Refactored web search tools using the unified registry system and new BaseTool.

This demonstrates how existing tools can be enhanced using the new
BaseTool pattern for better organization and discoverability.
"""

from enum import Enum
from typing import Dict, List, Any, Optional
from langchain_community.tools import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_core.documents import Document
import os
from pydantic import SecretStr

from quivr_core.llm_tools.base import SearchTool, ToolConfig
from quivr_core.llm_tools.registry import tool_registry, enhanced_register_tool


class WebSearchToolsList(str, Enum):
    TAVILY = "tavily"
    # Future tools can be added here
    # SERPER = "serper"
    # BING = "bing"


class TavilySearchToolConfig(ToolConfig):
    """Configuration for Tavily search tool."""

    api_key: str = ""
    max_results: int = 5
    search_depth: str = "advanced"
    include_answer: bool = True


@enhanced_register_tool(
    name=WebSearchToolsList.TAVILY,
    description="Tavily web search with advanced search capabilities",
    category="web_search",
    tags=["search", "web", "tavily", "research"],
    tool_type="search",
    config_schema=TavilySearchToolConfig,
)
class TavilySearchTool(SearchTool[TavilySearchToolConfig]):
    """Tavily web search tool implementing the new BaseTool interface."""

    TOOL_NAME = "tavily"
    TOOL_TYPE = "search"

    def __init__(
        self,
        config: Optional[TavilySearchToolConfig] = None,
        tool_name: Optional[str] = None,
    ):
        super().__init__(config=config, tool_name=tool_name)
        self.tavily_tool = None
        self._setup_tavily()

    def _setup_tavily(self):
        """Setup the Tavily tool instance."""
        api_key = self.config.api_key or os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError(
                "Missing required config key 'api_key' or environment variable 'TAVILY_API_KEY'"
            )

        tavily_api_wrapper = TavilySearchAPIWrapper(
            tavily_api_key=SecretStr(api_key),
        )

        # Extract config for Tavily
        tavily_config = {}
        if hasattr(self.config, "max_results"):
            tavily_config["max_results"] = self.config.max_results
        if hasattr(self.config, "search_depth"):
            tavily_config["search_depth"] = self.config.search_depth
        if hasattr(self.config, "include_answer"):
            tavily_config["include_answer"] = self.config.include_answer

        self.tavily_tool = TavilySearchResults(
            api_wrapper=tavily_api_wrapper, **tavily_config
        )
        self.tavily_tool.name = self.TOOL_NAME

    def validate_input(self, input_data: Any) -> None:
        """Validate search input."""
        super().validate_input(input_data)

        if isinstance(input_data, dict):
            if "query" not in input_data:
                raise ValueError("Search input dict must contain 'query' key")
        elif not isinstance(input_data, str):
            raise ValueError("Search input must be string or dict with 'query' key")

    def format_input(self, raw_input: Any) -> Dict[str, Any]:
        """Format input for Tavily search."""
        if isinstance(raw_input, dict):
            return raw_input
        elif isinstance(raw_input, str):
            return {"query": raw_input}
        else:
            return {"query": str(raw_input)}

    async def execute(self, input_data: Dict[str, Any], **kwargs) -> List[Document]:
        """Execute Tavily search and return formatted documents."""
        assert self.tavily_tool is not None, "Tavily tool not initialized"
        query = input_data.get("query", "")

        if hasattr(self.tavily_tool, "arun"):
            response = await self.tavily_tool.arun(query)
        else:
            response = self.tavily_tool.run(query)

        return self.format_output(response)

    def format_output(self, response: Any) -> List[Document]:
        """Format Tavily response as Document objects."""
        metadata = {"integration": "tavily", "integration_link": "https://tavily.com"}

        if isinstance(response, list):
            return [
                Document(
                    page_content=d.get("content", str(d)),
                    metadata={
                        **metadata,
                        "file_name": d.get("url", ""),
                        "original_file_name": d.get("url", ""),
                        "title": d.get("title", ""),
                        "score": d.get("score", 0.0),
                    },
                )
                for d in response
            ]
        else:
            return [Document(page_content=str(response), metadata=metadata)]


def list_web_search_tools() -> List[str]:
    """List all available web search tools."""
    return tool_registry.list_items(category="web_search")


def get_web_search_tool_info(tool_name: str) -> Dict[str, Any]:
    """Get detailed information about a web search tool."""
    metadata = tool_registry.get_metadata(tool_name)
    return {
        "name": metadata.name,
        "description": metadata.description,
        "category": metadata.category,
        "version": metadata.version,
        "tags": metadata.tags,
        "tool_type": metadata.tool_type,
    }
