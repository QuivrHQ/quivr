from uuid import UUID

from fastapi import APIRouter, Depends
from middlewares.auth import AuthBearer
from modules.notification.service.notification_service import NotificationService

notification_router = APIRouter()
notification_service = NotificationService()


@notification_router.get(
    "/notifications/{chat_id}",
    dependencies=[Depends(AuthBearer())],
    tags=["Notification"],
)
async def get_notifications(
    chat_id: UUID,
):
    """
    Get notifications by chat_id
    """

    return notification_service.get_chat_notifications(chat_id)
