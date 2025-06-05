from typing import Optional, Dict, Any, Tuple
from quivr_core.rag.entities.config import LLMEndpointConfig
from quivr_core.rag.langgraph_framework.nodes.base.base_node import (
    BaseNode,
    NodeValidationError,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_core.messages import HumanMessage, SystemMessage

from quivr_core.rag.prompts import TemplatePromptName
from quivr_core.rag.entities.prompt import PromptConfig


from quivr_core.rag.langgraph_framework.services.prompt_service import PromptService
from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.rag.langgraph_framework.nodes.base.extractors import ConfigExtractor
from quivr_core.rag.langgraph_framework.utils import reduce_rag_context


class GenerateChatLlmNode(BaseNode):
    """
    Node for generating a response using a Chat LLM model.
    """

    NODE_NAME = "generate_chat_llm"
    CONFIG_TYPES = (PromptConfig, LLMEndpointConfig)

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

    def get_config(
        self, config: Optional[Dict[str, Any]] = None
    ) -> Tuple[PromptConfig, LLMEndpointConfig]:
        """Extract and validate the filter history and LLM configs."""
        if config is None or not self.config_extractor:
            return PromptConfig(), LLMEndpointConfig()

        prompt_dict, llm_dict = self.config_extractor(config)

        return (
            PromptConfig.model_validate(prompt_dict),
            LLMEndpointConfig.model_validate(llm_dict),
        )

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
        # Get config using the injected extractor
        prompt_config, llm_config = self.get_config(config)

        messages = state["messages"]

        # Check if there is a system message in messages
        system_message = None
        user_message = None

        for msg in messages:
            if isinstance(msg, SystemMessage):
                system_message = str(msg.content)
            elif isinstance(msg, HumanMessage):
                user_message = str(msg.content)

        user_task = (
            user_message if user_message else (messages[0].content if messages else "")
        )

        # Prompt
        prompt = prompt_config.prompt

        final_inputs = {}
        final_inputs["task"] = user_task
        final_inputs["custom_instructions"] = prompt if prompt else "None"
        final_inputs["chat_history"] = state["chat_history"].to_list()

        # LLM
        llm = self.llm_service.get_base_llm()

        prompt = self.prompt_service.get_template(TemplatePromptName.CHAT_LLM_PROMPT)

        state, reduced_inputs = reduce_rag_context(
            state,
            final_inputs,
            system_message if system_message else prompt,
            self.llm_service.count_tokens,
            llm_config.max_context_tokens,
        )

        CHAT_LLM_PROMPT = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=str(system_message)),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessage(content=str(user_message)),
            ]
        )
        # Run
        chat_llm_prompt = CHAT_LLM_PROMPT.invoke(
            {"chat_history": final_inputs["chat_history"]}
        )
        response = llm.invoke(chat_llm_prompt)
        return {**state, "messages": [response]}
