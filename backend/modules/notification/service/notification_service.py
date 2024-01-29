from typing import List
from uuid import UUID

from models.settings import get_supabase_client
from modules.notification.dto.inputs import (
    CreateNotificationProperties,
    NotificationUpdatableProperties,
)
from modules.notification.entity.notification import Notification
from modules.notification.repository.notifications import Notifications
from modules.notification.repository.notifications_interface import (
    NotificationInterface,
)


class NotificationService:
    repository: NotificationInterface

    def __init__(self):
        supabase_client = get_supabase_client()
        self.repository = Notifications(supabase_client)

    def add_notification(self, notification: CreateNotificationProperties):
        """
        Add a notification
        """
        return self.repository.add_notification(notification)

    def get_chat_notifications(self, chat_id: UUID) -> List[Notification]:
        """
        Get notifications by chat_id
        """
        return self.repository.get_notifications_by_chat_id(chat_id)

    def remove_chat_notifications(self, chat_id: UUID) -> None:
        """
        Remove all notifications for a chat
        """
        self.repository.remove_notifications_by_chat_id(chat_id)

    def update_notification_by_id(
        self, notification_id, notification: NotificationUpdatableProperties
    ):
        """
        Update a notification
        """
        if notification:
            return self.repository.update_notification_by_id(
                notification_id, notification
            )
