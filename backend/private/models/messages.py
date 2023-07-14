from typing import List

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str = Field(
        ...,
        description="The role of the messages author. One of system, user, assistant, or function.",
    )
    content: str = Field(
        ...,
        description="The contents of the message. content is required for all messages, and may be null for assistant messages with function calls.",
    )


class Messages(BaseModel):
    messages: List[Message]
