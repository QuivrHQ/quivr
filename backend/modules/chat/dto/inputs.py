from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CreateChatHistory(BaseModel):
    chat_id: UUID
    user_message: str
    assistant: str
    prompt_id: Optional[UUID]
    brain_id: Optional[UUID]


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
