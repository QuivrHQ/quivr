from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from sqlmodel import TIMESTAMP, Column, Field, Relationship, SQLModel, text
from sqlmodel import UUID as PGUUID

from quivr_api.modules.user.entity.user_identity import User


class SyncsUser(BaseModel):
    id: int
    user_id: str
    name: str
    provider: str
    credentials: dict
    state: dict
    additional_data: dict


class SyncFile(BaseModel):
    name: str
    id: str
    is_folder: bool
    last_modified: str
    mime_type: str
    web_view_link: str
    notification_id: Optional[str] = None
    icon: Optional[str] = None
    parent_id: Optional[str] = None
    type: Optional[str] = None


class NotionSyncFile(SQLModel, table=True):
    """
    Represents a file synchronized with Notion.
    """

    __tablename__ = "notion_sync"  # type: ignore

    id: Optional[UUID] = Field(
        default=None,
        sa_column=Column(
            PGUUID,
            server_default=text("uuid_generate_v4()"),
            primary_key=True,
        ),
    )
    notion_id: str = Field(unique=True, description="The ID of the file in Notion")
    parent_id: str | None = Field(
        default=None, description="The ID of the parent file or directory"
    )
    name: str = Field(default=None, description="The name of the file")
    icon: Optional[str] = Field(description="The icon associated with the file")
    mime_type: str = Field(default=None, description="The MIME type of the file")
    web_view_link: str = Field(description="The web view link for the file")
    is_folder: bool = Field(description="Indicates if the file is a folder")
    last_modified: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True)),
        description="The last modified timestamp of the file",
    )
    type: Optional[str] = Field(
        default=None, description="The type/category of the file"
    )
    user_id: UUID = Field(
        foreign_key="users.id",
        description="The ID of the user who owns the file",
    )
    user: User = Relationship(back_populates="notion_syncs")


class SyncsActive(BaseModel):
    id: int
    name: str
    syncs_user_id: int
    user_id: str
    settings: dict
    last_synced: datetime
    sync_interval_minutes: int
    brain_id: str
    syncs_user: Optional[SyncsUser] = None
    notification_id: Optional[str] = None


class SyncsFiles(BaseModel):
    id: int
    path: str
    syncs_active_id: int
    last_modified: str
    brain_id: str
    supported: bool
