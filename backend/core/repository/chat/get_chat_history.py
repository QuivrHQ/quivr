from typing import List  # For type hinting

from models.chat import ChatHistory
from models.settings import common_dependencies


def get_chat_history(chat_id: str) -> List[ChatHistory]:
    commons = common_dependencies()
    history: List[ChatHistory] = commons["db"].get_chat_history(chat_id).data
    if history is None:
        return []
    else:
        return [
            ChatHistory(message)  # pyright: ignore reportPrivateUsage=none
            for message in history
        ]
