from abc import ABC, abstractmethod
from uuid import UUID

from modules.chat.dto.chats import ChatQuestion


class QAInterface(ABC):
    """
    Abstract class for all QA interfaces.
    This can be used to implement custom answer generation logic.
    """

    @abstractmethod
    def generate_answer(
        self,
        chat_id: UUID,
        question: ChatQuestion,
        save_answer: bool,
        *custom_params: tuple
    ):
        raise NotImplementedError(
            "generate_answer is an abstract method and must be implemented"
        )

    @abstractmethod
    def generate_stream(
        self,
        chat_id: UUID,
        question: ChatQuestion,
        save_answer: bool,
        *custom_params: tuple
    ):
        raise NotImplementedError(
            "generate_stream is an abstract method and must be implemented"
        )
