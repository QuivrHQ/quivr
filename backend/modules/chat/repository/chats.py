from models.settings import get_supabase_client
from modules.chat.dto.inputs import ChatMessageProperties
from modules.chat.entity.chat import Chat
from modules.chat.repository.chats_interface import ChatsInterface


class Chats(ChatsInterface):
    def __init__(self):
        supabase_client = get_supabase_client()
        self.db = supabase_client

    def create_chat(self, new_chat):
        response = self.db.table("chats").insert(new_chat).execute()
        return response

    def get_chat_by_id(self, chat_id: str):
        response = (
            self.db.from_("chats")
            .select("*")
            .filter("chat_id", "eq", chat_id)
            .execute()
        )
        return response

    def add_question_and_answer(self, chat_id, question_and_answer):
        response = (
            self.db.table("chat_history")
            .insert(
                {
                    "chat_id": str(chat_id),
                    "user_message": question_and_answer.question,
                    "assistant": question_and_answer.answer,
                }
            )
            .execute()
        ).data
        if len(response) > 0:
            response = Chat(response[0])

        return None

    def get_chat_history(self, chat_id: str):
        response = (
            self.db.from_("chat_history")
            .select("*")
            .filter("chat_id", "eq", chat_id)
            .order("message_time", desc=False)  # Add the ORDER BY clause
            .execute()
        )

        return response

    def get_user_chats(self, user_id):
        response = (
            self.db.from_("chats")
            .select("chat_id,user_id,creation_time,chat_name")
            .filter("user_id", "eq", user_id)
            .order("creation_time", desc=False)
            .execute()
        )
        return response

    def update_chat_history(self, chat_history):
        response = (
            self.db.table("chat_history")
            .insert(
                {
                    "chat_id": str(chat_history.chat_id),
                    "user_message": chat_history.user_message,
                    "assistant": chat_history.assistant,
                    "prompt_id": (
                        str(chat_history.prompt_id) if chat_history.prompt_id else None
                    ),
                    "brain_id": (
                        str(chat_history.brain_id) if chat_history.brain_id else None
                    ),
                    "metadata": chat_history.metadata if chat_history.metadata else {},
                }
            )
            .execute()
        )

        return response

    def update_chat(self, chat_id, updates):
        response = (
            self.db.table("chats").update(updates).match({"chat_id": chat_id}).execute()
        )

        return response

    def update_message_by_id(self, message_id, updates):
        response = (
            self.db.table("chat_history")
            .update(updates)
            .match({"message_id": message_id})
            .execute()
        )

        return response

    def delete_chat(self, chat_id):
        self.db.table("chats").delete().match({"chat_id": chat_id}).execute()

    def delete_chat_history(self, chat_id):
        self.db.table("chat_history").delete().match({"chat_id": chat_id}).execute()

    def update_chat_message(
        self, chat_id, message_id, chat_message_properties: ChatMessageProperties
    ):
        response = (
            self.db.table("chat_history")
            .update(chat_message_properties)
            .match({"message_id": message_id, "chat_id": chat_id})
            .execute()
        )

        return response
