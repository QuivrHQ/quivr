from dataclasses import dataclass
from typing import Optional

from logger import get_logger
from models.chat import Chat
from models.settings import common_dependencies

logger = get_logger(__name__)


@dataclass
class ChatUpdatableProperties:
    chat_name: Optional[str] = None

    def __init__(self, chat_name: Optional[str]):
        self.chat_name = chat_name


def update_chat(chat_id, chat_data: ChatUpdatableProperties) -> Chat:
    commons = common_dependencies()

    if not chat_id:
        logger.error("No chat_id provided")
        return  # pyright: ignore reportPrivateUsage=none

    updates = {}

    if chat_data.chat_name is not None:
        updates["chat_name"] = chat_data.chat_name

    updated_chat = None

    if updates:
        updated_chat = (
            commons["supabase"]
            .table("chats")
            .update(updates)
            .match({"chat_id": chat_id})
            .execute()
        ).data[0]
        logger.info(f"Chat {chat_id} updated")
    else:
        logger.info(f"No updates to apply for chat {chat_id}")
    return updated_chat  # pyright: ignore reportPrivateUsage=none
