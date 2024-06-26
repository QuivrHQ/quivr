from datetime import datetime
from typing import List
from uuid import UUID

from quivr_api.modules.brain.entity.brain_entity import Brain
from quivr_api.modules.user.entity.user_identity import User
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlmodel import JSON, TIMESTAMP
from sqlmodel import UUID as PGUUID
from sqlmodel import Column, Field, Relationship, SQLModel, text


class Chat(SQLModel, table=True):
    __tablename__ = "chats"  # type: ignore
    chat_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            PGUUID,
            server_default=text("uuid_generate_v4()"),
            primary_key=True,
        ),
    )
    chat_name: str | None
    creation_time: datetime | None = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=False),
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    user_id: UUID | None = Field(default=None, foreign_key="users.id")
    user: User | None = Relationship(back_populates="chats")  # type: ignore
    chat_history: List["ChatHistory"] | None = Relationship(back_populates="chat")  # type: ignore


class ChatHistory(AsyncAttrs, SQLModel, table=True):
    __tablename__ = "chat_history"  # type: ignore # type : ignore

    message_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            PGUUID,
            server_default=text("uuid_generate_v4()"),
            primary_key=True,
        ),
    )
    chat_id: UUID | None = Field(
        default=None,
        foreign_key="chats.chat_id",
        primary_key=True,
        nullable=False,  # Added nullable constraint
    )
    chat: Chat | None = Relationship(
        back_populates="chat_history", sa_relationship_kwargs={"lazy": "select"}
    )  # type: ignore
    user_message: str | None = None
    assistant: str | None = None
    message_time: datetime | None = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=False),
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    metadata_: dict | None = Field(
        default=None, sa_column=Column("metadata", JSON, default=None)
    )
    prompt_id: UUID | None = Field(default=None, foreign_key="prompts.id")
    brain_id: UUID | None = Field(
        default=None,
        foreign_key="brains.brain_id",
    )

    thumbs: bool | None = None
    brain: Brain | None = Relationship(
        back_populates="brain_chat_history", sa_relationship_kwargs={"lazy": "select"}
    )  # type: ignore

    class Config:
        # Note: Pydantic can't generate schema for arbitrary types
        arbitrary_types_allowed = True
