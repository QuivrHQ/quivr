from abc import ABC, abstractmethod
from uuid import UUID

from modules.chat.dto.chats import ChatQuestion


class QAInterface(ABC):
    """
    Abstract class for all QA interfaces.
    This can be used to implement custom answer generation logic.
    """

    @abstractmethod
    def calculate_pricing(self):
        raise NotImplementedError(
            "calculate_pricing is an abstract method and must be implemented"
        )

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

    def model_compatible_with_function_calling(self, model: str):
        if model in [
            "gpt-4o",
            "gpt-4-turbo",
            "gpt-4-turbo-2024-04-09",
            "gpt-4-turbo-preview",
            "gpt-4-0125-preview",
            "gpt-4-1106-preview",
            "gpt-4",
            "gpt-4-0613",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-0125",
            "gpt-3.5-turbo-1106",
            "gpt-3.5-turbo-0613",
        ]:
            return True
        return False
