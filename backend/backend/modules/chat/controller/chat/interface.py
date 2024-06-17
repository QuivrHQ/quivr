from abc import ABC, abstractmethod


class ChatInterface(ABC):
    @abstractmethod
    def get_answer_generator(
        self,
        chat_id,
        model,
        max_tokens,
        temperature,
        streaming,
        prompt_id,
        user_id,
        chat_question,
    ):
        pass
