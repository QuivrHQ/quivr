from typing import List  # For type hinting

from fastapi import HTTPException
from models.chat import ChatHistory
from models.settings import get_supabase_client


def update_chat_history(chat_id: str, user_message: str, assistant: str) -> ChatHistory:
    supabase_client = get_supabase_client()
    response: List[ChatHistory] = (
        supabase_client.table("chat_history")
        .insert(
            {
                "chat_id": str(chat_id),
                "user_message": user_message,
                "assistant": assistant,
            }
        )
        .execute()
    ).data
    if len(response) == 0:
        raise HTTPException(
            status_code=500, detail="An exception occurred while updating chat history."
        )
    return ChatHistory(response[0])  # pyright: ignore reportPrivateUsage=none
