from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from quivr_api.modules.chat.dto.inputs import (
    ChatMessageProperties,
    CreateChatHistory,
    QuestionAndAnswer,
)
from quivr_api.modules.chat.entity.chat import Chat


class ChatsInterface(ABC):
    @abstractmethod
    def create_chat(self, new_chat):
        """
        Insert a chat entry in "chats" db
        """
        pass

    @abstractmethod
    def get_chat_by_id(self, chat_id: str):
        """
        Get chat details by chat_id
        """
        pass

    @abstractmethod
    def add_question_and_answer(
        self, chat_id: UUID, question_and_answer: QuestionAndAnswer
    ) -> Optional[Chat]:
        """
        Add a question and answer to the chat history
        """
        pass

    @abstractmethod
    def get_chat_history(self, chat_id: str):
        """
        Get chat history by chat_id
        """
        pass

    @abstractmethod
    def get_user_chats(self, user_id: str):
        """
        Get all chats for a user
        """
        pass

    @abstractmethod
    def update_chat_history(self, chat_history: CreateChatHistory):
        """
        Update chat history
        """
        pass

    @abstractmethod
    def update_chat(self, chat_id, updates):
        """
        Update chat details
        """
        pass

    @abstractmethod
    def update_message_by_id(self, message_id, updates):
        """
        Update message details
        """
        pass

    @abstractmethod
    def delete_chat(self, chat_id):
        """
        Delete chat
        """
        pass

    @abstractmethod
    def delete_chat_history(self, chat_id):
        """
        Delete chat history
        """
        pass

    @abstractmethod
    def update_chat_message(
        self, chat_id, message_id, chat_message_properties: ChatMessageProperties
    ):
        """
        Update chat message
        """
        pass
