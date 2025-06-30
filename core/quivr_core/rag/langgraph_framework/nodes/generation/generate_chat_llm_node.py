from typing import Optional
from quivr_core.rag.entities.config import LLMEndpointConfig
from quivr_core.rag.langgraph_framework.base.node import BaseNode
from quivr_core.rag.langgraph_framework.base.exceptions import NodeValidationError
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage
from quivr_core.rag.langgraph_framework.base.graph_config import BaseGraphConfig
from quivr_core.rag.entities.prompt import PromptConfig
from quivr_core.rag.prompt.registry import get_prompt
from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.rag.langgraph_framework.utils import reduce_rag_context
from quivr_core.rag.langgraph_framework.registry.node_registry import register_node


@register_node(
    name="generate_chat_llm",
    description="Generate responses using a Chat LLM model with conversation context",
    category="generation",
    version="1.0.0",
    dependencies=["llm_service"],
)
class GenerateChatLlmNode(BaseNode):
    """
    Node for generating a response using a Chat LLM model.
    """

    NODE_NAME = "generate_chat_llm"

    def validate_input_state(self, state) -> None:
        """Validate that state has the required attributes and methods."""
        if "messages" not in state:
            raise NodeValidationError(
                "GenerateChatLlmNode requires 'messages' attribute in state"
            )
        if not state["messages"]:
            raise NodeValidationError(
                "GenerateChatLlmNode requires non-empty messages in state"
            )

        # Validate chat_history
        if "chat_history" not in state:
            raise NodeValidationError(
                "GenerateChatLlmNode requires 'chat_history' attribute in state"
            )

        # Validate chat_history has required methods
        chat_history = state["chat_history"]
        if not hasattr(chat_history, "to_list"):
            raise NodeValidationError(
                "GenerateChatLlmNode requires chat_history object with 'to_list' method"
            )

    def validate_output_state(self, state) -> None:
        """Validate that output has the correct attributes and methods."""
        pass

    async def execute(self, state, config: Optional[BaseGraphConfig] = None):
        """Execute the chat LLM generation."""
        # Get configs
        prompt_config = self.get_config(PromptConfig, config)
        llm_config = self.get_config(LLMEndpointConfig, config)

        # Get services through dependency injection
        llm_service = self.get_service(LLMService, llm_config)

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

        prompt = prompt_config.prompt

        final_inputs = {}
        final_inputs["task"] = user_task
        final_inputs["custom_instructions"] = prompt if prompt else "None"
        final_inputs["chat_history"] = state["chat_history"].to_list()

        # LLM
        llm = llm_service.get_base_llm()

        prompt_template = get_prompt("chat_llm")

        state, reduced_inputs = reduce_rag_context(
            state,
            final_inputs,
            system_message if system_message else prompt_template,
            llm_service.count_tokens,
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
