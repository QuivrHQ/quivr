from abc import ABC, abstractmethod
from uuid import UUID

from quivr_api.modules.notification.dto.inputs import (
    CreateNotification,
    NotificationUpdatableProperties,
)
from quivr_api.modules.notification.entity.notification import Notification


class NotificationInterface(ABC):
    @abstractmethod
    def add_notification(self, notification: CreateNotification) -> Notification:
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
    def remove_notification_by_id(self, notification_id: UUID):
        """
        Remove a notification by id
        Args:
            notification_id (UUID): The id of the notification

        Returns:
            str: Status message
        """
        pass
