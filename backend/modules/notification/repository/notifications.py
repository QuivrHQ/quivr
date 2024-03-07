from datetime import datetime, timedelta

from logger import get_logger
from modules.notification.dto.outputs import DeleteNotificationResponse
from modules.notification.entity.notification import Notification
from modules.notification.repository.notifications_interface import (
    NotificationInterface,
)

logger = get_logger(__name__)


class Notifications(NotificationInterface):
    def __init__(self, supabase_client):
        self.db = supabase_client

    def add_notification(self, notification):
        """
        Add a notification
        """
        response = (
            self.db.from_("notifications").insert(notification.dict()).execute()
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
            .update(notification.dict(exclude_unset=True))
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

        return DeleteNotificationResponse(
            status="deleted", notification_id=notification_id
        )

    def remove_notifications_by_chat_id(self, chat_id):
        """
        Remove all notifications for a chat
        Args:
            chat_id (UUID): The id of the chat
        """
        (
            self.db.from_("notifications")
            .delete()
            .filter("chat_id", "eq", chat_id)
            .execute()
        ).data

    def get_notifications_by_chat_id(self, chat_id):
        """
        Get all notifications for a chat
        Args:
            chat_id (UUID): The id of the chat

        Returns:
            list[Notification]: The notifications
        """
        five_minutes_ago = (datetime.now() - timedelta(minutes=5)).strftime(
            "%Y-%m-%d %H:%M:%S.%f"
        )

        notifications = (
            self.db.from_("notifications")
            .select("*")
            .filter("chat_id", "eq", chat_id)
            .filter("datetime", "gt", five_minutes_ago)
            .execute()
        ).data

        return [Notification(**notification) for notification in notifications]
