from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class StatusEnum(str, Enum):
    Pending = "Pending"
    Done = "Done"


class Notification(BaseModel):
    id: UUID
    datetime: str
    chat_id: Optional[UUID]
    message: Optional[str]
    action: str
    status: StatusEnum
