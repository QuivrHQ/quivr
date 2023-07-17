from fastapi import APIRouter
from logger import getLogger

logger = getLogger(__name__)

embeddings_router = APIRouter()


@embeddings_router.post("/embeddings", tags=["Embeddings"])
async def post_embeddings(
    model: str,
    input: str | list[str],
) -> str:
    logger.info(f"Received embeddings request for {model} with input {input}")

    return f"Hello from embeddings {model}!"
