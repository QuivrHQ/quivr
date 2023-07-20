from typing import List  # For type hinting

from fastapi import HTTPException
from models.chat import ChatHistory
from models.settings import common_dependencies


def update_chat_history(chat_id: str, user_message: str, assistant: str) -> ChatHistory:
    commons = common_dependencies()
    response: List[ChatHistory] = (
        commons["db"].update_chat_history(chat_id, user_message, assistant)
    ).data
    if len(response) == 0:
        raise HTTPException(
            status_code=500, detail="An exception occurred while updating chat history."
        )
    return ChatHistory(response[0])  # pyright: ignore reportPrivateUsage=none
