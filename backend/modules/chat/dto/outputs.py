from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class GetChatHistoryOutput(BaseModel):
    chat_id: UUID
    message_id: Optional[UUID] | str
    user_message: str
    assistant: str
    message_time: Optional[str]
    prompt_title: Optional[str] | None
    brain_name: Optional[str] | None

    def dict(self, *args, **kwargs):
        chat_history = super().dict(*args, **kwargs)
        chat_history["chat_id"] = str(chat_history.get("chat_id"))
        chat_history["message_id"] = str(chat_history.get("message_id"))

        return chat_history


class FunctionCall(BaseModel):
    arguments: str
    name: str


class ChatCompletionMessageToolCall(BaseModel):
    id: str
    function: FunctionCall
    type: str = "function"


class CompletionMessage(BaseModel):
    # = "assistant" | "user" | "system" | "tool"
    role: str
    content: str | None
    tool_calls: Optional[List[ChatCompletionMessageToolCall]]


class CompletionResponse(BaseModel):
    finish_reason: str
    message: CompletionMessage


class BrainCompletionOutput(BaseModel):
    messages: List[CompletionMessage]
    question: str
    response: CompletionResponse
