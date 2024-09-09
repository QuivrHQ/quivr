from quivr_api.modules.dependencies import get_supabase_client
from quivr_api.modules.notification.dto.inputs import (
    CreateNotification,
    NotificationUpdatableProperties,
)
from quivr_api.modules.notification.repository.notifications import Notifications
from quivr_api.modules.notification.repository.notifications_interface import (
    NotificationInterface,
)


class NotificationService:
    repository: NotificationInterface

    def __init__(self, repository: NotificationInterface | None = None):
        if repository is None:
            supabase_client = get_supabase_client()
            repository = Notifications(supabase_client)
        self.repository = repository

    def add_notification(self, notification: CreateNotification):
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

    def remove_notification_by_id(self, notification_id):
        """
        Remove a notification
        """
        return self.repository.remove_notification_by_id(notification_id)
