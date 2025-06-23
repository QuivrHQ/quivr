from typing import Optional

from quivr_core.rag.langgraph_framework.base.node import (
    BaseNode,
)
from quivr_core.rag.langgraph_framework.base.exceptions import NodeValidationError
from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.rag.langgraph_framework.entities.filter_history_config import (
    FilterHistoryConfig,
)
from quivr_core.rag.entities.config import LLMEndpointConfig
from uuid import uuid4
from quivr_core.rag.entities.chat import ChatHistory
from quivr_core.rag.langgraph_framework.base.graph_config import BaseGraphConfig
from quivr_core.rag.langgraph_framework.registry.node_registry import register_node


@register_node(
    name="filter_history",
    description="Filter chat history based on token limits and relevance",
    category="history",
    version="1.0.0",
    dependencies=["llm_service"],
)
class FilterHistoryNode(BaseNode):
    """
    Node for filtering the chat history.
    """

    NODE_NAME = "filter_history"

    def validate_input_state(self, state) -> None:
        """Validate that state has the required attributes and methods."""
        if "chat_history" not in state:
            raise NodeValidationError(
                "FilterHistoryNode requires 'chat_history' key in state"
            )

    def validate_output_state(self, state) -> None:
        """Validate that output has the correct attributes and methods."""
        pass

    async def execute(self, state, config: Optional[BaseGraphConfig] = None):
        """Filter chat history based on token limits and max history."""
        # Get configs
        history_config = self.get_config(FilterHistoryConfig, config)
        llm_config = self.get_config(LLMEndpointConfig, config)

        # Get services through dependency injection
        llm_service = self.get_service(LLMService, llm_config)

        chat_history = state["chat_history"]
        total_tokens = 0
        total_pairs = 0
        _chat_id = uuid4()
        _chat_history = ChatHistory(chat_id=_chat_id, brain_id=chat_history.brain_id)

        for human_message, ai_message in reversed(list(chat_history.iter_pairs())):
            message_tokens = llm_service.count_tokens(
                human_message.content
            ) + llm_service.count_tokens(ai_message.content)

            if (
                total_tokens + message_tokens > llm_config.max_context_tokens
                or total_pairs >= history_config.max_history
            ):
                break
            _chat_history.append(human_message)
            _chat_history.append(ai_message)
            total_tokens += message_tokens
            total_pairs += 1

        return {**state, "chat_history": _chat_history}
