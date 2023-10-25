from abc import ABC, abstractmethod


class ChatInterface(ABC):
    @abstractmethod
    def validate_authorization(self, user_id, required_roles):
        pass
