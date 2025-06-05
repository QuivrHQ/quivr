from typing import Optional, Dict, Any, Tuple

from quivr_core.rag.langgraph_framework.nodes.base.base_node import (
    BaseNode,
    NodeValidationError,
)
from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.rag.langgraph_framework.nodes.history.entity import FilterHistoryConfig
from quivr_core.rag.entities.config import LLMEndpointConfig
from uuid import uuid4
from quivr_core.rag.entities.chat import ChatHistory
from quivr_core.rag.langgraph_framework.nodes.base.extractors import ConfigExtractor


class FilterHistoryNode(BaseNode):
    """
    Node for filtering the chat history.
    Expected config types: (FilterHistoryConfig, LLMEndpointConfig)
    """

    NODE_NAME = "filter_history"
    CONFIG_TYPES = (FilterHistoryConfig, LLMEndpointConfig)

    def __init__(
        self,
        llm_service: LLMService,
        config_extractor: ConfigExtractor,
        node_name: Optional[str] = None,
    ):
        super().__init__(config_extractor=config_extractor, node_name=node_name)
        self.llm_service = llm_service

    def get_config(
        self, config: Optional[Dict[str, Any]] = None
    ) -> Tuple[FilterHistoryConfig, LLMEndpointConfig]:
        """Extract and validate the filter history and LLM configs."""
        if config is None or not self.config_extractor:
            return FilterHistoryConfig(), LLMEndpointConfig()

        history_dict, llm_dict = self.config_extractor(config)

        return (
            FilterHistoryConfig.model_validate(history_dict),
            LLMEndpointConfig.model_validate(llm_dict),
        )

    def validate_input_state(self, state) -> None:
        """Validate that state has the required attributes and methods."""

        if "chat_history" not in state:
            raise NodeValidationError(
                "FilterHistoryNode requires 'chat_history' key in state"
            )

    def validate_output_state(self, state) -> None:
        """Validate that output has the correct attributes and methods."""
        pass

    async def execute(self, state, config: Optional[Dict[str, Any]] = None):
        """
        Filter out the chat history to only include the messages that are relevant to the current question

        Takes in a chat_history= [HumanMessage(content='Qui est Chloé ? '),
        AIMessage(content="Chloé est une salariée travaillant pour l'entreprise Quivr en tant qu'AI Engineer,
        sous la direction de son supérieur hiérarchique, Stanislas Girard."),
        HumanMessage(content='Dis moi en plus sur elle'), AIMessage(content=''),
        HumanMessage(content='Dis moi en plus sur elle'),
        AIMessage(content="Désolé, je n'ai pas d'autres informations sur Chloé à partir des fichiers fournis.")]
        Returns a filtered chat_history with in priority: first max_tokens, then max_history where a Human message and an AI message count as one pair
        a token is 4 characters
        """

        # Get config using the injected extractor
        history_config, llm_config = self.get_config(config)

        chat_history = state["chat_history"]
        total_tokens = 0
        total_pairs = 0
        _chat_id = uuid4()
        _chat_history = ChatHistory(chat_id=_chat_id, brain_id=chat_history.brain_id)
        for human_message, ai_message in reversed(list(chat_history.iter_pairs())):
            # TODO: replace with tiktoken
            message_tokens = self.llm_service.count_tokens(
                human_message.content
            ) + self.llm_service.count_tokens(ai_message.content)

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
