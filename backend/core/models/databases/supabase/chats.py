from models.databases.repository import Repository


class Chats(Repository):
    def __init__(self, supabase_client):
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

    def get_chat_history(self, chat_id: str):
        reponse = (
            self.db.from_("chat_history")
            .select("*")
            .filter("chat_id", "eq", chat_id)
            .order("message_time", desc=False)  # Add the ORDER BY clause
            .execute()
        )

        return reponse

    def get_user_chats(self, user_id: str):
        response = (
            self.db.from_("chats")
            .select("chat_id,user_id,creation_time,chat_name")
            .filter("user_id", "eq", user_id)
            .execute()
        )
        return response

    def update_chat_history(self, chat_id: str, user_message: str, assistant: str):
        response = (
            self.db.table("chat_history")
            .insert(
                {
                    "chat_id": str(chat_id),
                    "user_message": user_message,
                    "assistant": assistant,
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

    def get_chat_details(self, chat_id):
        response = (
            self.db.from_("chats")
            .select("*")
            .filter("chat_id", "eq", chat_id)
            .execute()
        )
        return response

    def delete_chat(self, chat_id):
        self.db.table("chats").delete().match({"chat_id": chat_id}).execute()

    def delete_chat_history(self, chat_id):
        self.db.table("chat_history").delete().match({"chat_id": chat_id}).execute()
