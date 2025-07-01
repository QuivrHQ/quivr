from typing import Optional, List
from quivr_core.rag.entities.config import LLMEndpointConfig
from quivr_core.rag.langgraph_framework.base.node import (
    BaseNode,
)
from quivr_core.rag.langgraph_framework.base.exceptions import NodeValidationError
from langgraph.types import Send
from quivr_core.rag.entities.prompt import PromptConfig
from quivr_core.rag.langgraph_framework.base.graph_config import BaseGraphConfig
from quivr_core.rag.prompt.registry import get_prompt
from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.rag.langgraph_framework.entities.routing_entity import (
    SplittedInputWithInstructions,
)
from quivr_core.rag.langgraph_framework.task import UserTasks
from quivr_core.rag.langgraph_framework.registry.node_registry import register_node


@register_node(
    name="routing",
    description="Route user input to appropriate processing paths",
    category="routing",
    version="1.0.0",
    dependencies=["llm_service"],
)
class RoutingNode(BaseNode):
    """
    Node for routing user input to appropriate processing paths.
    """

    NODE_NAME = "routing"

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

        # Validate chat_history since it's used in execution
        if "chat_history" not in state:
            raise NodeValidationError(
                "RoutingNode requires 'chat_history' attribute in state"
            )

        # Validate chat_history has required methods
        chat_history = state["chat_history"]
        if not hasattr(chat_history, "to_list"):
            raise NodeValidationError(
                "RoutingNode requires chat_history object with 'to_list' method"
            )

    def validate_output_state(self, state) -> None:
        """Validate that output has the correct attributes and methods."""
        pass

    async def execute(self, state, config: Optional[BaseGraphConfig] = None):
        """Execute routing logic."""
        # Get configs
        prompt_config = self.get_config(PromptConfig, config)
        llm_config = self.get_config(LLMEndpointConfig, config)

        # Get services through dependency injection
        llm_service = self.get_service(LLMService, llm_config)

        # Use prompt registry directly instead of prompt service
        prompt = get_prompt("split_input")

        # Get chat history for the prompt (it's accessed later anyway)
        chat_history = state.get("chat_history")
        if hasattr(chat_history, "to_list"):
            chat_history_list = chat_history.to_list()
        else:
            chat_history_list = []

        msg = prompt.format(
            user_input=state["messages"][0].content, chat_history=chat_history_list
        )

        response: SplittedInputWithInstructions = (
            await llm_service.invoke_with_structured_output(
                msg, SplittedInputWithInstructions
            )
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
