from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class NotificationsStatusEnum(str, Enum):
    Pending = "Pending"
    Done = "Done"


class Notification(BaseModel):
    id: UUID
    datetime: str
    chat_id: Optional[UUID]
    message: Optional[str]
    action: str
    status: NotificationsStatusEnum

    def dict(self, *args, **kwargs):
        notification_dict = super().dict(*args, **kwargs)
        if notification_dict.get("chat_id"):
            notification_dict["chat_id"] = str(notification_dict.get("chat_id"))
        return notification_dict
