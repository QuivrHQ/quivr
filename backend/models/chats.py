from typing import List, Optional, Tuple
from uuid import UUID

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
    model: Optional[str]
    temperature: Optional[float]
    max_tokens: Optional[int]
    brain_id: Optional[UUID]
    prompt_id: Optional[UUID]
