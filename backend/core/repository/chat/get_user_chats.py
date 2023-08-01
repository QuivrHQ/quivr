from typing import List

from models.chat import Chat
from models.settings import get_supabase_client


def get_user_chats(user_id: str) -> List[Chat]:
    supabase_client = get_supabase_client()
    response = (
        supabase_client.from_("chats")
        .select("chat_id,user_id,creation_time,chat_name")
        .filter("user_id", "eq", user_id)
        .execute()
    )
    chats = [Chat(chat_dict) for chat_dict in response.data]
    return chats
