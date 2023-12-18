from uuid import UUID

from pydantic import BaseModel


class SharedChat(BaseModel):
    id: UUID
    chat_id: UUID
