from typing import Optional
from uuid import UUID

from modules.notification.entity.notification import NotificationsStatusEnum
from pydantic import BaseModel


class CreateNotificationProperties(BaseModel):
    """Properties that can be received on notification creation"""

    chat_id: Optional[UUID] = None
    message: Optional[str] = None
    action: str
    status: NotificationsStatusEnum = NotificationsStatusEnum.Pending

    def dict(self, *args, **kwargs):
        notification_dict = super().dict(*args, **kwargs)
        if notification_dict.get("chat_id"):
            notification_dict["chat_id"] = str(notification_dict.get("chat_id"))
        return notification_dict


class NotificationUpdatableProperties(BaseModel):
    """Properties that can be received on notification update"""

    message: Optional[str] = None
    status: Optional[NotificationsStatusEnum] = NotificationsStatusEnum.Done
