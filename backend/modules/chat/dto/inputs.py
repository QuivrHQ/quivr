from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CreateChatHistory(BaseModel):
    chat_id: UUID
    user_message: str
    assistant: str
    prompt_id: Optional[UUID] = None
    brain_id: Optional[UUID] = None
    metadata: Optional[dict] = {}


class QuestionAndAnswer(BaseModel):
    question: str
    answer: str


@dataclass
class CreateChatProperties:
    name: str

    def __init__(self, name: str):
        self.name = name


@dataclass
class ChatUpdatableProperties:
    chat_name: Optional[str] = None

    def __init__(self, chat_name: Optional[str]):
        self.chat_name = chat_name


class ChatMessageProperties(BaseModel, extra="ignore"):
    thumbs: Optional[bool]

    def dict(self, *args, **kwargs):
        chat_dict = super().dict(*args, **kwargs)
        if chat_dict.get("thumbs"):
            # Set thumbs to boolean value or None if not present
            chat_dict["thumbs"] = bool(chat_dict["thumbs"])
        return chat_dict
