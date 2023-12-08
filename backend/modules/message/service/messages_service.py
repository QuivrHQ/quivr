from typing import List
from uuid import UUID

from modules.message.dto.inputs import CreateMessageProperties, UpdateMessageProperties
from modules.message.entity.message import Message
from modules.message.repository.messages import Messages
from modules.message.repository.messages_interface import MessagesInterface


class MessagesService:
    repository: MessagesInterface

    def __init__(self):
        self.repository = Messages()

    def get_messages_brain(
        self, user_id: UUID, brain_id: UUID
    ) -> List[Message] | List[None]:
        """Update user onboarding information by user_id"""

        return self.repository.get_messages_brain(user_id, brain_id)

    def update_message(
        self, user_id: UUID, message: UpdateMessageProperties
    ) -> Message | None:
        """Update user onboarding information by user_id"""

        return self.repository.update_message(user_id, message)

    def remove_message(self, user_id: UUID, message_id: UUID) -> Message | None:
        """Update user onboarding information by user_id"""

        return self.repository.remove_message(user_id, message_id)

    def create_message(
        self, user_id: UUID, message_create: CreateMessageProperties
    ) -> Message:
        """Update user onboarding information by user_id"""

        return self.repository.create_message(user_id, message_create)
