from fastapi import APIRouter


shared_chat_router = APIRouter()


@shared_chat_router.get("/shared/chat")
def get_shared_chat_identity_route() -> str:
    """
    Get user identity.
    """
    return "abc"
