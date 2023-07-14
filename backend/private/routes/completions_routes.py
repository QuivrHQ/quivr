from typing import List

from fastapi import APIRouter

completions_router = APIRouter()


@completions_router.post("/chat/completions", tags=["Chat Completions"])
async def post_chat_completions(
    model: str,  # make union of all models
    messages: List[
        str
    ],  # eg [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Hello!"}]
) -> str:
    return f"Hello from {model}!"
