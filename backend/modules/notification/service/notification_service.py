from models.settings import get_supabase_client
from modules.notification.dto.inputs import NotificationUpdatableProperties
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

    def add_notification(self, notification: Notification):
        """
        Add a notification
        """
        return self.repository.add_notification(notification)

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
