from datetime import datetime
from typing import Any, Generator, Tuple
from uuid import UUID, uuid4

from langchain_core.messages import AIMessage, HumanMessage
from quivr_core.models import ChatMessage


class ChatHistory:
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
        # Reverse the chat_history, newest first
        it = iter(self.get_chat_history(newest_first=True))
        for ai_message, human_message in zip(it, it):
            assert isinstance(
                human_message.msg, HumanMessage
            ), f"msg {human_message} is not HumanMessage"
            assert isinstance(
                ai_message.msg, AIMessage
            ), f"msg {human_message} is not AIMessage"
            yield (human_message.msg, ai_message.msg)
