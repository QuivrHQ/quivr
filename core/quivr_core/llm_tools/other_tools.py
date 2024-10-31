from enum import Enum
from typing import Dict, Any, Type, Union
from langchain_core.tools import BaseTool
from quivr_core.llm_tools.entity import ToolsCategory
from quivr_core.rag.entities.models import cited_answer


class OtherToolsList(str, Enum):
    CITED_ANSWER = "cited_answer"


def create_other_tool(tool_name: str, config: Dict[str, Any]) -> Union[BaseTool, Type]:
    if tool_name == OtherToolsList.CITED_ANSWER:
        return cited_answer
    else:
        raise ValueError(f"Tool {tool_name} is not supported.")


OtherTools = ToolsCategory(
    name="Other",
    description="Other tools",
    tools=[OtherToolsList.CITED_ANSWER],
    create_tool=create_other_tool,
)
