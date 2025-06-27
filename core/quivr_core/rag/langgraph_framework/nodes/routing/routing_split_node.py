from typing import Optional
from quivr_core.rag.entities.config import LLMEndpointConfig, RetrievalConfig
from quivr_core.rag.langgraph_framework.base.node import (
    BaseNode,
)
from quivr_core.rag.langgraph_framework.base.exceptions import NodeValidationError
from langgraph.types import Send
from quivr_core.rag.prompts import TemplatePromptName
from quivr_core.rag.entities.prompt import PromptConfig
from quivr_core.rag.langgraph_framework.base.graph_config import BaseGraphConfig
from quivr_core.rag.langgraph_framework.services.rag_prompt_service import (
    RAGPromptService,
)
from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.rag.langgraph_framework.entities.routing_entity import (
    SplittedInputWithInstructions,
)
from quivr_core.rag.langgraph_framework.task import UserTasks
from quivr_core.rag.langgraph_framework.registry.node_registry import register_node


@register_node(
    name="routing_split",
    description="Split and route user input into multiple processing paths",
    category="routing",
    version="1.0.0",
    dependencies=["llm_service", "prompt_service"],
)
class RoutingSplitNode(BaseNode):
    """
    Node for splitting and routing user input.
    """

    NODE_NAME = "routing_split"

    def validate_input_state(self, state) -> None:
        """Validate that state has the required attributes and methods."""
        if "messages" not in state:
            raise NodeValidationError(
                "RoutingSplitNode requires 'messages' attribute in state"
            )
        if not state["messages"]:
            raise NodeValidationError(
                "RoutingSplitNode requires non-empty messages in state"
            )

        # Validate chat_history
        if "chat_history" not in state:
            raise NodeValidationError(
                "RoutingSplitNode requires 'chat_history' attribute in state"
            )

        # Validate chat_history has required methods
        chat_history = state["chat_history"]
        if not hasattr(chat_history, "to_list"):
            raise NodeValidationError(
                "RoutingSplitNode requires chat_history object with 'to_list' method"
            )

    def validate_output_state(self, state) -> None:
        """Validate that output has the correct attributes and methods."""
        pass

    async def execute(self, state, config: Optional[BaseGraphConfig] = None):
        """Execute routing split logic."""
        # Get configs
        prompt_config = self.get_config(PromptConfig, config)
        llm_config = self.get_config(LLMEndpointConfig, config)
        retrieval_config = self.get_config(RetrievalConfig, config)

        # Get services through dependency injection
        llm_service = self.get_service(LLMService, llm_config)
        prompt_service = self.get_service(RAGPromptService, retrieval_config)

        prompt = prompt_service.get_template(TemplatePromptName.SPLIT_PROMPT)

        msg = prompt.format(
            chat_history=state["chat_history"].to_list(),
            user_input=state["messages"][0].content,
        )

        response: SplittedInputWithInstructions = (
            await llm_service.invoke_with_structured_output(
                msg, SplittedInputWithInstructions
            )
        )

        instructions = response.instructions or prompt_config.prompt
        tasks = UserTasks(response.task_list) if response.task_list else None

        if instructions:
            return [
                Send(
                    "edit_system_prompt",
                    {**state, "instructions": instructions, "tasks": tasks},
                )
            ]
        elif tasks:
            return [Send("filter_history", {**state, "tasks": tasks})]

        return []
