from typing import Optional, Dict, Any, List
from quivr_core.rag.langgraph_framework.nodes.base.base_node import (
    BaseNode,
    NodeValidationError,
)
from langgraph.types import Send


from quivr_core.rag.prompts import TemplatePromptName
from quivr_core.rag.entities.prompt import PromptConfig


from quivr_core.rag.langgraph_framework.services.prompt_service import PromptService
from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.rag.langgraph_framework.nodes.base.extractors import ConfigExtractor
from quivr_core.rag.langgraph_framework.nodes.routing.entity import SplittedInput
from quivr_core.rag.langgraph_framework.task import UserTasks


class RoutingNode(BaseNode):
    """
    Node for generating a response using a Chat LLM model.
    """

    NODE_NAME = "routing"
    CONFIG_TYPES = (PromptConfig,)

    def __init__(
        self,
        prompt_service: PromptService,
        llm_service: LLMService,
        config_extractor: ConfigExtractor,
        node_name: Optional[str] = None,
    ):
        super().__init__(config_extractor, node_name)
        self.prompt_service = prompt_service
        self.llm_service = llm_service

    def get_config(self, config: Optional[Dict[str, Any]] = None) -> PromptConfig:
        """Extract and validate the filter history and LLM configs."""
        if config is None or not self.config_extractor:
            return PromptConfig()

        prompt_dict, llm_dict = self.config_extractor(config)

        return PromptConfig.model_validate(prompt_dict)

    def validate_input_state(self, state) -> None:
        """Validate that state has the required attributes and methods."""

        if "messages" not in state:
            raise NodeValidationError(
                "RetrieveNode requires 'messages' attribute in state"
            )

        if not state["messages"]:
            raise NodeValidationError(
                "RetrieveNode requires non-empty messages in state"
            )

    def validate_output_state(self, state) -> None:
        """Validate that output has the correct attributes and methods."""
        pass

    async def execute(self, state, config: Optional[Dict[str, Any]] = None):
        """
        The routing function for the RAG model.

        Args:
            state (AgentState): The current state of the agent.

        Returns:
            dict: The next state of the agent.
        """

        prompt_config = self.get_config(config)

        prompt = self.prompt_service.get_template(TemplatePromptName.SPLIT_PROMPT)

        msg = prompt.format(
            user_input=state["messages"][0].content,
        )

        response: SplittedInput

        response = await self.llm_service.invoke_with_structured_output(
            msg, SplittedInput
        )

        send_list: List[Send] = []

        instructions = (
            response.instructions if response.instructions else prompt_config.prompt
        )

        if instructions:
            send_list.append(Send("edit_system_prompt", {"instructions": instructions}))
        elif response.task_list:
            chat_history = state["chat_history"]
            send_list.append(
                Send(
                    "filter_history",
                    {
                        "chat_history": chat_history,
                        "tasks": UserTasks(response.task_list),
                    },
                )
            )

        return send_list
