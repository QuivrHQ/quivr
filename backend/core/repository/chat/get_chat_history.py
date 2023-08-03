from typing import List

from models.chat import ChatHistory
from models.settings import get_supabase_db  # For type hinting


def get_chat_history(chat_id: str) -> List[ChatHistory]:
    supabase_db = get_supabase_db()
    history: List[ChatHistory] = supabase_db.get_chat_history(chat_id).data
    if history is None:
        return []
    else:
        return [
            ChatHistory(message)  # pyright: ignore reportPrivateUsage=none
            for message in history
        ]
