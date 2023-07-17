from typing import List

from models.chat import Chat
from models.settings import common_dependencies


def get_user_chats(user_id: str) -> List[Chat]:
    commons = common_dependencies()
    response = (
        commons["supabase"]
        .from_("chats")
        .select("chat_id,user_id,creation_time,chat_name")
        .filter("user_id", "eq", user_id)
        .execute()
    )
    chats = [Chat(chat_dict) for chat_dict in response.data]
    return chats
