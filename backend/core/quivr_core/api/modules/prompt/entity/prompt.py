from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel
from sqlmodel import UUID as PGUUID
from sqlmodel import Column, Field, Relationship, SQLModel, text


class PromptStatusEnum(str, Enum):
    private = "private"
    public = "public"


class Prompt(SQLModel, table=True):
    __tablename__ = "prompts"  # type: ignore
    id: UUID | None = Field(
        default=None,
        sa_column=Column(
            PGUUID,
            server_default=text("uuid_generate_v4()"),
            primary_key=True,
        ),
    )
    content: str | None = None
    title: str | None = Field(default=None, max_length=255)
    status: str = Field(default="private", max_length=255)
    brain: List["Brain"] = Relationship(  # noqa: F821
        back_populates="prompt", sa_relationship_kwargs={"lazy": "joined"}
    )


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
