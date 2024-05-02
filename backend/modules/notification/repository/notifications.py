from logger import get_logger
from modules.notification.dto.inputs import CreateNotification
from modules.notification.entity.notification import Notification
from modules.notification.repository.notifications_interface import (
    NotificationInterface,
)

logger = get_logger(__name__)


class Notifications(NotificationInterface):
    def __init__(self, supabase_client):
        self.db = supabase_client

    def add_notification(self, notification: CreateNotification):
        """
        Add a notification
        """
        response = (
            self.db.from_("notifications").insert(notification.model_dump()).execute()
        ).data
        return Notification(**response[0])

    def update_notification_by_id(
        self,
        notification_id,
        notification,
    ):
        if notification_id is None:
            logger.info("Notification id is required")
            return None

        """Update a notification by id"""
        response = (
            self.db.from_("notifications")
            .update(notification.model_dump(exclude_unset=True))
            .filter("id", "eq", notification_id)
            .execute()
        ).data

        if response == []:
            logger.info(f"Notification with id {notification_id} not found")
            return None

        return Notification(**response[0])

    def remove_notification_by_id(self, notification_id):
        """
        Remove a notification by id
        Args:
            notification_id (UUID): The id of the notification

        Returns:
            str: Status message
        """
        response = (
            self.db.from_("notifications")
            .delete()
            .filter("id", "eq", notification_id)
            .execute()
            .data
        )

        if response == []:
            logger.info(f"Notification with id {notification_id} not found")
            return None

        return {"status": "success"}
