from typing import List  # For type hinting

from models.chat import ChatHistory
from models.settings import get_supabase_client


def get_chat_history(chat_id: str) -> List[ChatHistory]:
    supabase_client = get_supabase_client()
    history: List[ChatHistory] = (
        supabase_client.from_("chat_history")
        .select("*")
        .filter("chat_id", "eq", chat_id)
        .order("message_time", desc=False)  # Add the ORDER BY clause
        .execute()
    ).data
    if history is None:
        return []
    else:
        return [
            ChatHistory(message)  # pyright: ignore reportPrivateUsage=none
            for message in history
        ]
