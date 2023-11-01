from uuid import UUID
from repository.shared_chat import (
    get_shared_chat_by_shared_chat_id,
)
from fastapi import APIRouter


shared_chat_router = APIRouter()


@shared_chat_router.get("/shared/chat/{shared_chat_id}")
def get_shared_chat_identity_route(shared_chat_id: UUID) -> str:
    """
    Get user identity.
    """
    return get_shared_chat_by_shared_chat_id(shared_chat_id)
