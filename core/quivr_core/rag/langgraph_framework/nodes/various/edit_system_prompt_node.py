"""
System prompt editing node with runtime validation.
"""

import logging
from typing import Optional
from quivr_core.rag.entities.config import LLMEndpointConfig, WorkflowConfig
from quivr_core.rag.entities.prompt import PromptConfig
from quivr_core.rag.langgraph_framework.base.graph_config import BaseGraphConfig
from quivr_core.rag.langgraph_framework.base.node import BaseNode
from quivr_core.rag.langgraph_framework.base.exceptions import NodeValidationError
from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.rag.prompt.registry import get_prompt
from quivr_core.rag.langgraph_framework.utils import update_active_tools
from quivr_core.rag.langgraph_framework.state import UpdatedPromptAndTools
from quivr_core.rag.utils import collect_tools
from quivr_core.rag.langgraph_framework.registry.node_registry import register_node

logger = logging.getLogger("quivr_core")


@register_node(
    name="edit_system_prompt",
    description="Edit system prompts and manage tool activation based on user instructions",
    category="various",
    version="1.0.0",
    dependencies=["llm_service"],
)
class EditSystemPromptNode(BaseNode):
    """
    Node for editing the system prompt.

    Runtime Requirements: State must have:
    - instructions: str (for reading instructions)
    - system_prompt: str (for reading system prompt)
    - available_tools: list[str] (for reading available tools)
    - activated_tools: list[str] (for reading activated tools)
    """

    NODE_NAME = "edit_system_prompt"

    def validate_input_state(self, state) -> None:
        """Validate that state has the required attributes and methods."""
        if "instructions" not in state:
            raise NodeValidationError(
                "EditSystemPromptNode requires 'instructions' attribute in state"
            )

        if not state["instructions"]:
            raise NodeValidationError(
                "EditSystemPromptNode requires non-empty instructions in state"
            )

    def validate_output_state(self, state) -> None:
        """Validate that output has the correct attributes and methods."""
        pass

    async def execute(self, state, config: Optional[BaseGraphConfig] = None):
        """Execute document retrieval for all user tasks."""
        # Get configs
        llm_config = self.get_config(LLMEndpointConfig, config)
        workflow_config = self.get_config(WorkflowConfig, config)
        prompt_config = self.get_config(PromptConfig, config)

        # Get services through dependency injection
        llm_service = self.get_service(LLMService, llm_config)

        user_instruction = state["instructions"]
        prompt = prompt_config.prompt
        available_tools, activated_tools = collect_tools(workflow_config)
        inputs = {
            "instruction": user_instruction,
            "system_prompt": prompt if prompt else "",
            "available_tools": available_tools,
            "activated_tools": activated_tools,
        }

        update_prompt_template = get_prompt("update_system_prompt")
        msg = update_prompt_template.format(**inputs)

        response: UpdatedPromptAndTools = (
            await llm_service.invoke_with_structured_output(msg, UpdatedPromptAndTools)
        )

        update_active_tools(workflow_config, response)
        prompt_config.prompt = response.prompt

        reasoning = [response.prompt_reasoning] if response.prompt_reasoning else []
        reasoning += [response.tools_reasoning] if response.tools_reasoning else []

        return {**state, "messages": [], "reasoning": reasoning}
