from uuid import UUID

from pydantic import BaseModel


class Message(BaseModel):
    """Response when getting messages"""

    message_id: UUID
    brain_id: UUID
    user_id: UUID
    content: str
    created_at: str
