from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from modules.message.dto.inputs import CreateMessageProperties, UpdateMessageProperties
from modules.message.entity.message import Message


class MessagesInterface(ABC):
    @abstractmethod
    def get_messages_brain(
        self, user_id: UUID, brain: UUID
    ) -> List[Message] | List[None]:
        """
        Get messages by user_id and brain_id
        """
        pass

    @abstractmethod
    def update_message(
        self, user_id: UUID, update: UpdateMessageProperties
    ) -> Message | None:
        """Update user onboarding information by user_id"""
        pass

    @abstractmethod
    def remove_message(self, user_id: UUID, message_id: UUID) -> Message | None:
        """
        Remove message by user_id and message_id
        """
        pass

    @abstractmethod
    def create_message(
        self, user_id: UUID, message_create: CreateMessageProperties
    ) -> Message:
        """
        Create user onboarding information by user_id
        """
        pass
