from dataclasses import dataclass
from uuid import UUID

from logger import get_logger
from models import Chat, get_supabase_db

logger = get_logger(__name__)


@dataclass
class CreateChatProperties:
    name: str

    def __init__(self, name: str):
        self.name = name


def create_chat(user_id: UUID, chat_data: CreateChatProperties) -> Chat:
    supabase_db = get_supabase_db()

    # Chat is created upon the user's first question asked
    logger.info(f"New chat entry in chats table for user {user_id}")

    # Insert a new row into the chats table
    new_chat = {
        "user_id": str(user_id),
        "chat_name": chat_data.name,
    }
    insert_response = supabase_db.create_chat(new_chat)
    logger.info(f"Insert response {insert_response.data}")

    return insert_response.data[0]
