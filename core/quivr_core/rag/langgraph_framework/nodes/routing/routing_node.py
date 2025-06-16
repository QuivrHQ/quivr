from typing import Optional, List
from quivr_core.rag.entities.config import LLMEndpointConfig, RetrievalConfig
from quivr_core.rag.langgraph_framework.nodes.base.node import (
    BaseNode,
    NodeValidationError,
)
from langgraph.types import Send
from quivr_core.rag.prompts import TemplatePromptName
from quivr_core.rag.entities.prompt import PromptConfig
from quivr_core.rag.langgraph_framework.nodes.base.graph_config import BaseGraphConfig
from quivr_core.rag.langgraph_framework.services.prompt_service import PromptService
from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.rag.langgraph_framework.nodes.base.extractors import ConfigExtractor
from quivr_core.rag.langgraph_framework.nodes.routing.entity import SplittedInput
from quivr_core.rag.langgraph_framework.task import UserTasks


class RoutingNode(BaseNode):
    """
    Node for routing user input to appropriate processing paths.
    """

    NODE_NAME = "routing"
    CONFIG_TYPES = (PromptConfig,)

    def __init__(
        self,
        prompt_service: Optional[PromptService] = None,
        llm_service: Optional[LLMService] = None,
        config_extractor: Optional[ConfigExtractor] = None,
        node_name: Optional[str] = None,
    ):
        super().__init__(config_extractor, node_name)

        self.prompt_service = prompt_service
        self._prompt_service_user_provided = prompt_service is not None

        self.llm_service = llm_service
        self._llm_service_user_provided = llm_service is not None

    def validate_input_state(self, state) -> None:
        """Validate that state has the required attributes and methods."""
        if "messages" not in state:
            raise NodeValidationError(
                "RoutingNode requires 'messages' attribute in state"
            )

        if not state["messages"]:
            raise NodeValidationError(
                "RoutingNode requires non-empty messages in state"
            )

    def validate_output_state(self, state) -> None:
        """Validate that output has the correct attributes and methods."""
        pass

    async def execute(self, state, config: Optional[BaseGraphConfig] = None):
        """Execute routing logic."""
        # Type-safe config extraction
        prompt_config, _ = self.get_config(PromptConfig, config)

        retrieval_config, retrieval_config_changed = self.get_config(
            RetrievalConfig, config
        )
        if not self.prompt_service or (
            not self._prompt_service_user_provided and retrieval_config_changed
        ):
            self.logger.debug(
                "Initializing/reinitializing PromptService due to config change"
            )
            self.prompt_service = PromptService(retrieval_config=retrieval_config)
        assert self.prompt_service

        llm_config, llm_config_changed = self.get_config(LLMEndpointConfig, config)
        # Initialize LLMService if needed
        if not self.llm_service or (
            not self._llm_service_user_provided and llm_config_changed
        ):
            self.logger.debug(
                "Initializing/reinitializing LLMService due to config change"
            )
            self.llm_service = LLMService(llm_config=llm_config)
        assert self.llm_service

        prompt = self.prompt_service.get_template(TemplatePromptName.SPLIT_PROMPT)

        msg = prompt.format(
            user_input=state["messages"][0].content,
        )

        response: SplittedInput = await self.llm_service.invoke_with_structured_output(
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
