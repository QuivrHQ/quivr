from uuid import UUID

from pydantic import BaseModel


class DeleteNotificationResponse(BaseModel):
    """Response when deleting a prompt"""

    status: str = "delete"
    notification_id: UUID
