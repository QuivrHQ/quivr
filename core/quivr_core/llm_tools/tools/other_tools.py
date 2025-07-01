"""
Other tools using the new tool registry system and BaseTool pattern.
"""

from enum import Enum
from typing import Dict, Any, Optional

from quivr_core.llm_tools.base import QuivrBaseTool, ToolConfig
from quivr_core.llm_tools.registry import enhanced_register_tool
from quivr_core.rag.entities.models import cited_answer as CitedAnswerModel


class OtherToolsList(str, Enum):
    CITED_ANSWER = "cited_answer"


class CitedAnswerToolConfig(ToolConfig):
    """Configuration for cited answer tool."""

    pass  # Uses base ToolConfig for now


@enhanced_register_tool(
    name=OtherToolsList.CITED_ANSWER,
    description="Tool for generating cited answers with sources and follow-up questions",
    category="other",
    tool_type="processing",
    config_schema=CitedAnswerToolConfig,
    tags=["citation", "answer", "sources"],
)
class CitedAnswerTool(QuivrBaseTool):
    """Tool that provides the cited_answer Pydantic model for structured LLM output."""

    TOOL_NAME = "cited_answer"
    TOOL_TYPE = "processing"

    def __init__(
        self,
        config: Optional[CitedAnswerToolConfig] = None,
        tool_name: Optional[str] = None,
    ):
        super().__init__(config=config, tool_name=tool_name)

    def validate_input(self, input_data: Any) -> None:
        """Validate input for cited answer tool."""
        if not isinstance(input_data, dict):
            raise ValueError("CitedAnswerTool input must be a dictionary")

        required_fields = ["answer", "citations", "followup_questions"]
        for field in required_fields:
            if field not in input_data:
                raise ValueError(f"Missing required field: {field}")

    async def execute(self, input_data: Dict[str, Any], **kwargs) -> CitedAnswerModel:
        """Execute the cited answer tool."""
        # Create and validate the cited answer model
        return CitedAnswerModel(
            answer=input_data["answer"],
            citations=input_data["citations"],
            followup_questions=input_data["followup_questions"],
        )

    def format_output(self, raw_output: CitedAnswerModel) -> CitedAnswerModel:
        """Format output - return the model directly."""
        return raw_output

    def get_pydantic_model(self) -> type:
        """Get the Pydantic model for LLM tool binding."""
        return CitedAnswerModel
