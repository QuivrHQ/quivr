from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Column
from sqlmodel import JSON, Field, Relationship, SQLModel

from backend.modules.user.entity.user_identity import User


class Chat(SQLModel, table=True):
    __tablename__ = "chats"  # type: ignore

    chat_id: UUID | None = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    chat_name: str | None
    chat_history: JSON | None = Field(default_factory=dict, sa_column=Column(JSON))
    created_at: datetime | None = Field(default_factory=datetime.utcnow)
    user_id: UUID | None = Field(default=None, foreign_key="users.id")
    user: User | None = Relationship(back_populates="chats")  # type: ignore

    # Note: depreciated but for sqlmodel isn't compatible yet
    class Config:
        # Note: Pydantic can't generate schema for arbitrary types
        arbitrary_types_allowed = True


class ChatHistory(SQLModel, table=True):
    __tablename__ = "chat_history"  # type: ignore

    chat_id: UUID = Field(primary_key=True, default_factory=uuid4)
    message_id: UUID
    user_message: str | None
    assistant: str
    message_time: str
    prompt_id: Optional[UUID]
    brain_id: Optional[UUID]
    metadata_: dict | None = Field(sa_column=Column("metadata", JSON, default=None))
    thumbs: Optional[bool] = None
