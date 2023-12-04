from abc import ABC, abstractmethod
from uuid import UUID

from modules.notification.dto.inputs import (
    CreateNotificationProperties,
    NotificationUpdatableProperties,
)
from modules.notification.dto.outputs import DeleteNotificationResponse
from modules.notification.entity.notification import Notification


class NotificationInterface(ABC):
    @abstractmethod
    def add_notification(
        self, notification: CreateNotificationProperties
    ) -> Notification:
        """
        Add a notification
        """
        pass

    @abstractmethod
    def update_notification_by_id(
        self, notification_id: UUID, notification: NotificationUpdatableProperties
    ) -> Notification:
        """Update a notification by id"""
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def remove_notifications_by_chat_id(self, chat_id: UUID) -> None:
        """
        Remove all notifications for a chat
        Args:
            chat_id (UUID): The id of the chat
        """
        pass

    @abstractmethod
    def get_notifications_by_chat_id(self, chat_id: UUID) -> list[Notification]:
        """
        Get all notifications for a chat
        Args:
            chat_id (UUID): The id of the chat

        Returns:
            list[Notification]: The notifications
        """
        pass
