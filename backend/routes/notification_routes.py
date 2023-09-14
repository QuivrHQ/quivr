from uuid import UUID

from auth import AuthBearer
from fastapi import APIRouter, Depends
from repository.notification.get_chat_notifications import (
    get_chat_notifications,
)

notification_router = APIRouter()


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

    return get_chat_notifications(chat_id)
