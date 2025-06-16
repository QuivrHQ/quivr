"""
Basic document retrieval node with runtime validation.
"""

import logging
from typing import Optional
from quivr_core.rag.entities.config import LLMEndpointConfig, WorkflowConfig
from quivr_core.rag.entities.prompt import PromptConfig
from quivr_core.rag.langgraph_framework.nodes.base.graph_config import BaseGraphConfig
from quivr_core.rag.langgraph_framework.nodes.base.node import (
    BaseNode,
)

from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.rag.langgraph_framework.services.prompt_service import PromptService
from quivr_core.rag.entities.retriever import RetrieverConfig
from quivr_core.rag.langgraph_framework.nodes.base.extractors import ConfigExtractor
from quivr_core.rag.langgraph_framework.utils import update_active_tools
from quivr_core.rag.prompts import TemplatePromptName
from quivr_core.rag.langgraph_framework.state import UpdatedPromptAndTools
from quivr_core.rag.utils import collect_tools

logger = logging.getLogger("quivr_core")


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
    CONFIG_TYPES = (RetrieverConfig,)

    def __init__(
        self,
        llm_service: Optional[LLMService] = None,
        prompt_service: Optional[PromptService] = None,
        config_extractor: Optional[ConfigExtractor] = None,
        node_name: Optional[str] = None,
    ):
        super().__init__(config_extractor, node_name)

        self.llm_service = llm_service
        self._llm_service_user_provided = llm_service is not None

        self.prompt_service = prompt_service
        self._prompt_service_user_provided = prompt_service is not None

    def validate_input_state(self, state) -> None:
        """Validate that state has the required attributes and methods."""
        pass

    def validate_output_state(self, state) -> None:
        """Validate that output has the correct attributes and methods."""
        pass

    async def execute(self, state, config: Optional[BaseGraphConfig] = None):
        """Execute document retrieval for all user tasks."""

        retriever_config, retriever_config_changed = self.get_config(
            RetrieverConfig, config
        )

        llm_config, llm_config_changed = self.get_config(LLMEndpointConfig, config)

        workflow_config, _ = self.get_config(WorkflowConfig, config)

        prompt_config, _ = self.get_config(PromptConfig, config)

        # Initialize LLMService if needed
        if not self.llm_service or (
            not self._llm_service_user_provided and llm_config_changed
        ):
            self.logger.debug(
                "Initializing/reinitializing LLMService due to config change"
            )
            self.llm_service = LLMService(llm_config=llm_config)
        assert self.llm_service

        # Initialize PromptService if needed
        if not self.prompt_service:
            self.logger.debug(
                "Initializing/reinitializing PromptService due to config change"
            )
            self.prompt_service = PromptService()
        assert self.prompt_service

        user_instruction = state["instructions"]
        prompt = prompt_config.prompt
        available_tools, activated_tools = collect_tools(workflow_config)
        inputs = {
            "instruction": user_instruction,
            "system_prompt": prompt if prompt else "",
            "available_tools": available_tools,
            "activated_tools": activated_tools,
        }

        msg = self.prompt_service.get_template(TemplatePromptName.UPDATE_PROMPT).format(
            **inputs
        )

        response: UpdatedPromptAndTools = (
            await self.llm_service.invoke_with_structured_output(
                msg, UpdatedPromptAndTools
            )
        )

        update_active_tools(workflow_config, response)
        prompt_config.prompt = response.prompt

        reasoning = [response.prompt_reasoning] if response.prompt_reasoning else []
        reasoning += [response.tools_reasoning] if response.tools_reasoning else []

        return {**state, "messages": [], "reasoning": reasoning}
