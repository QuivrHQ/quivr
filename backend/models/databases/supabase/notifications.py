from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from models.databases.repository import Repository
from models.notifications import Notification, NotificationsStatusEnum
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


class DeleteNotificationResponse(BaseModel):
    """Response when deleting a prompt"""

    status: str = "delete"
    notification_id: UUID


class NotificationUpdatableProperties(BaseModel):
    """Properties that can be received on notification update"""

    message: Optional[str]
    status: Optional[NotificationsStatusEnum] = NotificationsStatusEnum.Done


class Notifications(Repository):
    def __init__(self, supabase_client):
        self.db = supabase_client

    def add_notification(
        self, notification: CreateNotificationProperties
    ) -> Notification:
        """
        Add a notification
        """
        response = (
            self.db.from_("notifications").insert(notification.dict()).execute()
        ).data
        return Notification(**response[0])

    def update_notification_by_id(
        self, notification_id: UUID, notification: NotificationUpdatableProperties
    ) -> Notification:
        """Update a notification by id"""
        response = (
            self.db.from_("notifications")
            .update(notification.dict(exclude_unset=True))
            .filter("id", "eq", notification_id)
            .execute()
        ).data

        if response == []:
            raise HTTPException(404, "Notification not found")

        return Notification(**response[0])

    def remove_notification_by_id(
        self, notification_id: UUID
    ) -> DeleteNotificationResponse:
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
            raise HTTPException(404, "Notification not found")

        return DeleteNotificationResponse(
            status="deleted", notification_id=notification_id
        )

    def remove_notifications_by_chat_id(self, chat_id: UUID) -> None:
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

    def get_notifications_by_chat_id(self, chat_id: UUID) -> list[Notification]:
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
