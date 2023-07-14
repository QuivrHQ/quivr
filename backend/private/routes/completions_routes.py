from fastapi import APIRouter
from logger import get_logger
from models.messages import Messages

logger = get_logger(__name__)

completions_router = APIRouter()


@completions_router.post("/chat/completions", tags=["Chat Completions"])
async def post_chat_completions(
    model: str,  # make union of all models
    messages: Messages,
) -> str:
    logger.info(
        f"Received chat completions request for {model} with messages {messages}"
    )
    return f"Hello from {model}!"
