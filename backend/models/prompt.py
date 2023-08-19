from enum import Enum
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
