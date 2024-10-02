from enum import Enum
from langchain_community.tools import TavilySearchResults
from quivr_core.models import cited_answer


class AvailableLLMTools(str, Enum):
    TAVILY = "tavily"
    CITED_ANSWER = "cited_answer"


class LLMToolFactory:
    @staticmethod
    def create_tool(tool_name: str, config: dict):
        if tool_name == AvailableLLMTools.TAVILY:
            return TavilySearchResults(
                max_results=config.get("max_results", 5),
                search_depth=config.get("search_depth", "advanced"),
                include_answer=config.get("include_answer", True),
            )
        elif tool_name == AvailableLLMTools.CITED_ANSWER:
            return cited_answer
        else:
            raise ValueError(f"Tool {tool_name} is not supported.")
