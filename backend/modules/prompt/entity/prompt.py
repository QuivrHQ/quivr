from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class PromptStatusEnum(str, Enum):
    private = "private"
    public = "public"


class Prompt(BaseModel):
    title: str
    content: str
    status: PromptStatusEnum = PromptStatusEnum.private
    id: UUID


class CreatePromptProperties(BaseModel):
    """Properties that can be received on prompt creation"""

    title: str
    content: str
    status: PromptStatusEnum = PromptStatusEnum.private


class PromptUpdatableProperties(BaseModel):
    """Properties that can be received on prompt update"""

    title: Optional[str] = None
    content: Optional[str] = None
    status: Optional[PromptStatusEnum] = None


class DeletePromptResponse(BaseModel):
    """Response when deleting a prompt"""

    status: str = "delete"
    prompt_id: UUID
