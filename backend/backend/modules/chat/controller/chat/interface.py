from abc import ABC, abstractmethod


class ChatInterface(ABC):
    @abstractmethod
    def validate_authorization(self, user_id, required_roles):
        pass

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
