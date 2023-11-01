from uuid import UUID
from typing import List
from repository.shared_chat import create_shared_chat
from models.databases.supabase.shared_chats import CreateSharedChatProperties

# from repository.chat.get_chat_history_with_notifications import ChatItem
from repository.shared_chat import (
    get_shared_chat_by_id,
)
from repository.chat.get_chat_history_with_notifications import (
    ChatItem,
    get_chat_history_with_notifications,
)
from fastapi import APIRouter


shared_chat_router = APIRouter()


@shared_chat_router.get("/shared/chat/{shared_chat_id}")
def get_shared_chat_identity_route(shared_chat_id: UUID) -> List[ChatItem]:
    """
    Get user identity.
    """
    chat_id = get_shared_chat_by_id(shared_chat_id)
    # chat = get_chat_by_id(chat_id)
    # chat_history = get_chat_history(chat_id)

    return get_chat_history_with_notifications(chat_id)


@shared_chat_router.post("/shared/chat/")
async def create_shared_chat_route(
    createSharedChatProps: CreateSharedChatProperties,
    # current_user: UserIdentity = Depends(get_current_user),
):
    new_shared_chat = create_shared_chat(createSharedChatProps)

    return new_shared_chat
