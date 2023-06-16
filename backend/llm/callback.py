import asyncio

from langchain.callbacks.base import BaseCallbackHandler
from logger import get_logger

logger = get_logger(__name__)


class StreamingCallbackHandler(BaseCallbackHandler):
    def __init__(self, queue: asyncio.Queue):
        self.queue = queue

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        try:
            logger.info("Putting token in queue: %s", token)
            self.queue.put_nowait(token)
        except asyncio.QueueFull:
            logger.error("Queue is full, dropping token: %s", token)
