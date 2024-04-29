from enum import Enum
from typing import List, Optional, Tuple, Union
from uuid import UUID

from modules.chat.dto.outputs import GetChatHistoryOutput
from modules.notification.entity.notification import Notification
from pydantic import BaseModel


class ChatMessage(BaseModel):
    model: str
    question: str
    # A list of tuples where each tuple is (speaker, text)
    history: List[Tuple[str, str]]
    temperature: float = 0.0
    max_tokens: int = 256
    use_summarization: bool = False
    chat_id: Optional[UUID] = None
    chat_name: Optional[str] = None


class ChatQuestion(BaseModel):
    question: str
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    brain_id: Optional[UUID] = None
    prompt_id: Optional[UUID] = None


class Sources(BaseModel):
    name: str
    source_url: str
    type: str
    original_file_name: str
    citation: str


class ChatItemType(Enum):
    MESSAGE = "MESSAGE"
    NOTIFICATION = "NOTIFICATION"


class ChatItem(BaseModel):
    item_type: ChatItemType
    body: Union[GetChatHistoryOutput, Notification]
