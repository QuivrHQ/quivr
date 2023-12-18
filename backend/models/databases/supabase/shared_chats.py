from models.shared_chat import SharedChat
from logger import get_logger
from models.databases.repository import Repository
from pydantic import BaseModel

logger = get_logger(__name__)


class CreateSharedChatProperties(BaseModel):
    chat_id: str


class SharedChats(Repository):
    def __init__(self, supabase_client):
        self.db = supabase_client

    def create_shared_chat(self, shared_chat: CreateSharedChatProperties) -> SharedChat:
        """
        Create a shared chat
        """

        response = (self.db.table("shared_chats").insert(shared_chat.dict())).execute()
        return SharedChat(**response.data[0])
