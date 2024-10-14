from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel
from quivr_api.modules.brain.entity.brain_user import BrainUserDB
from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"  # type: ignore

    id: UUID | None = Field(
        primary_key=True,
        nullable=False,
        default_factory=uuid4,
    )
    email: str
    onboarded: bool | None = None
    chats: List["Chat"] | None = Relationship(back_populates="user")  # type: ignore
    notion_syncs: List["NotionSyncFile"] | None = Relationship(back_populates="user")  # type: ignore
    brains: List["Brain"] = Relationship(
        back_populates="users",
        link_model=BrainUserDB,
    )


class UserIdentity(BaseModel):
    id: UUID
    email: Optional[str] = None
    username: Optional[str] = None
    company: Optional[str] = None
    onboarded: Optional[bool] = None
    company_size: Optional[str] = None
    usage_purpose: Optional[str] = None
