from typing import List

from fastapi import APIRouter, Depends
from middlewares.auth import (  # Assuming you have a get_current_user function
    AuthBearer,
    get_current_user,
)
from modules.message.dto.inputs import CreateMessageProperties, UpdateMessageProperties
from modules.message.entity.message import Message
from modules.message.service.messages_service import MessagesService
from modules.user.entity.user_identity import UserIdentity

messages_router = APIRouter()

messages_services = MessagesService()


@messages_router.get(
    "/messages",
    dependencies=[Depends(AuthBearer())],
    tags=["Messages"],
)
async def get_messages_user_brain(
    brain_id: str,
    current_user: UserIdentity = Depends(get_current_user),
) -> List[Message] | List[None]:
    """
    Get users messages information for the current user and brain
    """

    return messages_services.get_messages_brain(current_user.id, brain_id)


@messages_router.put(
    "/messages",
    dependencies=[Depends(AuthBearer())],
    tags=["Messages"],
)
async def update_messages_brain(
    message: UpdateMessageProperties,
    current_user: UserIdentity = Depends(get_current_user),
) -> Message | None:
    """
    Update user message information for the current user
    """

    return messages_services.update_message(current_user.id, message)


@messages_router.delete(
    "/messages",
    dependencies=[Depends(AuthBearer())],
    tags=["Messages"],
)
async def delete_messages_brain(
    message_id: str,
    current_user: UserIdentity = Depends(get_current_user),
) -> Message | None:
    """
    Delete user message for the current user with message_id
    """

    return messages_services.remove_message(current_user.id, message_id)


@messages_router.post(
    "/messages",
    dependencies=[Depends(AuthBearer())],
    tags=["Messages"],
)
async def create_messages_brain(
    message: CreateMessageProperties,
    current_user: UserIdentity = Depends(get_current_user),
) -> Message | None:
    """
    Create user message for the current user
    """

    return messages_services.create_message(current_user.id, message)
