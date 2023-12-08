from models.settings import get_supabase_client
from modules.message.entity.message import Message

from .messages_interface import MessagesInterface


class Messages(MessagesInterface):
    def __init__(self):
        supabase_client = get_supabase_client()
        self.db = supabase_client

    def get_messages_brain(self, user_id, brain_id):
        """
        Get user messages information by user_id and brain_id
        """
        messages_data = (
            self.db.from_("messages")
            .select("*")
            .match({"user_id": str(user_id), "brain_id": str(brain_id)})
            .execute()
        ).data

        if messages_data == []:
            return []

        messages = []
        for message in messages_data:
            messages.append(Message(**message))

        return messages

    def update_message(self, user_id, update):
        """
        Update user messages information by user_id and message_id
        """
        response = (
            self.db.table("messages")
            .update({"content": update.content})
            .match({"user_id": str(user_id), "message_id": str(update.message_id)})
            .execute()
        )

        if len(response.data) == 0:
            return None
        return Message(**response.data[0])

    def remove_message(self, user_id, message_id):
        """
        Remove message by user_id and message_id
        """
        response = (
            self.db.table("messages")
            .delete()
            .match({"user_id": str(user_id), "message_id": str(message_id)})
            .execute()
        )

        if len(response.data) == 0:
            return None
        return Message(**response.data[0])

    def create_message(self, user_id, message_create):
        """
        Create user messages information by user_id
        """
        response = (
            self.db.table("messages")
            .insert(
                [
                    {
                        "brain_id": str(message_create.brain_id),
                        "user_id": str(user_id),
                        "content": message_create.content,
                    }
                ]
            )
            .execute()
        )
        return Message(**response.data[0])
