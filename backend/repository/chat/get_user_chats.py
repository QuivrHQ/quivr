from typing import List

from models.chat import Chat
from models.settings import common_dependencies


def get_user_chats(user_id: str) -> List[Chat]:
    commons = common_dependencies()
    response = commons["db"].get_user_chats(user_id)
    chats = [Chat(chat_dict) for chat_dict in response.data]
    return chats
