import asyncio
import os
from typing import AsyncIterable, Awaitable

from auth.auth_bearer import AuthBearer, get_current_user
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from logger import get_logger
from models.chats import ChatMessage
from models.settings import CommonsDep
from models.users import User

logger = get_logger(__name__)

stream_router = APIRouter()

openai_api_key = os.getenv("OPENAI_API_KEY")


async def send_message(chat_message: ChatMessage) -> AsyncIterable[str]:
    callback = AsyncIteratorCallbackHandler()

    streaming_llm = ChatOpenAI(
        temperature=0,
        model_name=chat_message.model,
        streaming=True,
        callbacks=[callback],
    )

    async def wrap_done(fn: Awaitable, event: asyncio.Event):
        """Wrap an awaitable with a event to signal when it's done or an exception is raised."""
        try:
            resp = await fn
            logger.debug("Done: %s", resp)
        except Exception as e:
            # TODO: handle exception
            print(f"Caught exception: {e}")
        finally:
            # Signal the aiter to stop.
            event.set()

    task = asyncio.create_task(
        wrap_done(
            streaming_llm.agenerate(
                messages=[[HumanMessage(content=chat_message.question)]]
            ),
            callback.done,
        )
    )

    async for token in callback.aiter():
        logger.info("Token: %s", token)
        # Use server-sent-events to stream the response
        yield f"data: {token}\n\n"

    await task


@stream_router.post("/stream", dependencies=[Depends(AuthBearer())], tags=["Stream"])
def stream(
    chat_message: ChatMessage,
):
    return StreamingResponse(
        send_message(chat_message),
        media_type="text/event-stream",
    )
