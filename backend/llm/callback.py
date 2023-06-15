from langchain.callbacks.base import BaseCallbackHandler
from logger import get_logger

logger = get_logger(__name__)


class StreamingCallbackHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        logger.info(f"My custom handler, token: {token}")
