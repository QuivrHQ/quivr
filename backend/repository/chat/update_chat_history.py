from models.chat import ChatHistory
from models.settings import common_dependencies
from typing import List  # For type hinting
from fastapi import HTTPException


def update_chat_history(
    chat_id: str, user_message: str, assistant_answer: str
) -> ChatHistory:
    commons = common_dependencies()
    response: List[ChatHistory] = (
        commons["supabase"]
        .table("chat_history")
        .insert(
            {
                "chat_id": str(chat_id),
                "user_message": user_message,
                "assistant": assistant_answer,
            }
        )
        .execute()
    ).data
    if len(response) == 0:
        raise HTTPException(
            status_code=500, detail="An exception occurred while updating chat history."
        )
    return response[0]
