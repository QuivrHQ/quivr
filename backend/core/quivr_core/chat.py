from copy import deepcopy
from datetime import datetime
from typing import Any, Generator, List, Tuple
from uuid import UUID, uuid4

from langchain_core.messages import AIMessage, HumanMessage

from quivr_core.models import ChatMessage


class ChatHistory:
    """
    Chat history is a list of ChatMessage.
    It is used to store the chat history of a chat.
    """

    def __init__(self, chat_id: UUID, brain_id: UUID | None) -> None:
        self.id = chat_id
        self.brain_id = brain_id
        # TODO(@aminediro): maybe use a deque() instead ?
        self._msgs: list[ChatMessage] = []

    def get_chat_history(self, newest_first: bool = False):
        """Returns a ChatMessage list sorted by time

        Returns:
            list[ChatMessage]: list of chat messages
        """
        history = sorted(self._msgs, key=lambda msg: msg.message_time)
        if newest_first:
            return history[::-1]
        return history

    def __len__(self):
        return len(self._msgs)

    def append(
        self, langchain_msg: AIMessage | HumanMessage, metadata: dict[str, Any] = {}
    ):
        """
        Append a message to the chat history.
        """
        chat_msg = ChatMessage(
            chat_id=self.id,
            message_id=uuid4(),
            brain_id=self.brain_id,
            msg=langchain_msg,
            message_time=datetime.now(),
            metadata=metadata,
        )
        self._msgs.append(chat_msg)

    def iter_pairs(self) -> Generator[Tuple[HumanMessage, AIMessage], None, None]:
        """
        Iterate over the chat history as pairs of HumanMessage and AIMessage.
        """
        # Reverse the chat_history, newest first
        it = iter(self.get_chat_history(newest_first=True))
        for ai_message, human_message in zip(it, it, strict=False):
            assert isinstance(
                human_message.msg, HumanMessage
            ), f"msg {human_message} is not HumanMessage"
            assert isinstance(
                ai_message.msg, AIMessage
            ), f"msg {human_message} is not AIMessage"
            yield (human_message.msg, ai_message.msg)

    def to_list(self) -> List[HumanMessage | AIMessage]:
        """Format the chat history into a list of HumanMessage and AIMessage"""
        return [_msg.msg for _msg in self._msgs]

    def __deepcopy__(self, memo):
        """
        Support for deepcopy of ChatHistory.
        This method ensures that mutable objects (like lists) are copied deeply.
        """
        # Create a new instance of ChatHistory
        new_copy = ChatHistory(self.id, deepcopy(self.brain_id, memo))

        # Perform a deepcopy of the _msgs list
        new_copy._msgs = deepcopy(self._msgs, memo)

        # Return the deep copied instance
        return new_copy
