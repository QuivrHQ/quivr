from uuid import UUID

from .brainful_chat import BrainfulChat
from .brainless_chat import BrainlessChat


def get_chat_strategy(brain_id: UUID | None = None):
    if brain_id:
        return BrainfulChat()
    else:
        return BrainlessChat()
