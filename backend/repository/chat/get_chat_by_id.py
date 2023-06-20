from models.settings import common_dependencies
from dataclasses import dataclass
from typing import Optional
from models.chats import ChatHistory


@dataclass
class Chat:
    chat_id: str
    user_id: str
    creation_time: str
    history: ChatHistory
    chat_name: str

    def __init__(self, chat_dict: dict):
        self.chat_id = chat_dict.get("chat_id")
        self.user_id = chat_dict.get("user_id")
        self.creation_time = chat_dict.get("creation_time")
        self.history = chat_dict.get("history", [])
        self.chat_name = chat_dict.get("chat_name")


def get_chat_by_id(chat_id) -> Optional[Chat]:
    commons = common_dependencies()
    chats = (
        commons["supabase"]
        .from_("chats")
        .select("*")
        .filter("chat_id", "eq", chat_id)
        .execute()
    ).data
    print("chats", chats)
    if len(chats) > 0:
        return Chat(chats[0])
    else:
        return None
