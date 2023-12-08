from uuid import UUID

from pydantic import BaseModel


class CreateMessageProperties(BaseModel):

    """Properties that can be received on message creation"""

    brain_id: UUID
    content: str

    class Config:
        extra = "forbid"


class UpdateMessageProperties(BaseModel):

    """Properties that can be received on message update"""

    message_id: UUID
    content: str

    class Config:
        extra = "forbid"
