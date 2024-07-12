from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class NotificationsStatusEnum(str, Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


class Notification(BaseModel):
    id: UUID
    user_id: UUID
    bulk_id: Optional[UUID] = None
    status: NotificationsStatusEnum
    title: str
    description: Optional[str]
    archived: Optional[bool] = False
    read: Optional[bool] = False
    datetime: Optional[datetime]  # timestamp
    category: Optional[str]
    brain_id: Optional[str]
