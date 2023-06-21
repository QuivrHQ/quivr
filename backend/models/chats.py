from typing import List, Optional, Tuple
from uuid import UUID
from dataclasses import dataclass

from pydantic import BaseModel


class ChatMessage(BaseModel):
    model: str = "gpt-3.5-turbo-16k"
    question: str
    # A list of tuples where each tuple is (speaker, text)
    history: List[Tuple[str, str]]
    temperature: float = 0.0
    max_tokens: int = 256
    use_summarization: bool = False
    chat_id: Optional[UUID] = None
    chat_name: Optional[str] = None


class ChatQuestion(BaseModel):
    model: str = "gpt-3.5-turbo-0613"
    question: str
    temperature: float = 0.0
    max_tokens: int = 256


class ChatAttributes(BaseModel):
    chat_name: Optional[str] = None


@dataclass
class ChatHistory:
    chat_id: str
    message_id: str
    user_message: str
    assistant: str
    message_time: str

    def __init__(self, chat_dict: dict):
        self.chat_id = chat_dict.get("chat_id")
        self.message_id = chat_dict.get("message_id")
        self.user_message = chat_dict.get("user_message")
        self.assistant = chat_dict.get("assistant")
        self.message_time = chat_dict.get("message_time")


@dataclass
class CreateChat:
    name: str
