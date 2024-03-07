from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class GetChatHistoryOutput(BaseModel):
    chat_id: UUID
    message_id: Optional[UUID] | str
    user_message: str
    assistant: str
    message_time: Optional[str] = None
    prompt_title: Optional[str] | None = None
    brain_name: Optional[str] | None = None
    brain_id: Optional[str] | None = (
        None  # string because UUID is not JSON serializable
    )
    metadata: Optional[dict] | None = None

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
    content: str | None = None
    tool_calls: Optional[List[ChatCompletionMessageToolCall]] = None


class CompletionResponse(BaseModel):
    finish_reason: str
    message: CompletionMessage


class BrainCompletionOutput(BaseModel):
    messages: List[CompletionMessage]
    question: str
    response: CompletionResponse
