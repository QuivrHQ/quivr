from models.chat import ChatHistory
from models.settings import common_dependencies
from typing import List  # For type hinting


def get_chat_history(chat_id: str) -> List[ChatHistory]:
    commons = common_dependencies()
    history: List[ChatHistory] = (
        commons["supabase"]
        .from_("chat_history")
        .select("*")
        .filter("chat_id", "eq", chat_id)
        .order("message_time", desc=False)  # Add the ORDER BY clause
        .execute()
    ).data
    if history is None:
        return []
    else:
        return [ChatHistory(message) for message in history]
