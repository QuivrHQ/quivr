from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel
from quivr_core.models import KnowledgeStatus
from sqlalchemy import JSON, TIMESTAMP, Column, text
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlmodel import UUID as PGUUID
from sqlmodel import Field, Relationship, SQLModel

from quivr_api.modules.knowledge.entity.knowledge_brain import KnowledgeBrain


class KnowledgeSource(str, Enum):
    LOCAL = "local"
    WEB = "web"
    GDRIVE = "google drive"
    DROPBOX = "dropbox"
    SHAREPOINT = "sharepoint"


class Knowledge(BaseModel):
    id: UUID
    file_size: int = 0
    status: KnowledgeStatus
    file_name: Optional[str] = None
    url: Optional[str] = None
    extension: str = ".txt"
    is_folder: bool = False
    updated_at: datetime
    created_at: datetime
    source: Optional[str] = None
    source_link: Optional[str] = None
    file_sha1: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None
    user_id: Optional[UUID] = None
    brains: List[Dict[str, Any]]
    parent: Optional["Knowledge"]
    children: Optional[list["Knowledge"]]


class KnowledgeUpdate(BaseModel):
    file_name: Optional[str] = None
    status: Optional[KnowledgeStatus] = None
    url: Optional[str] = None
    file_sha1: Optional[str] = None
    extension: Optional[str] = None
    parent_id: Optional[UUID] = None
    source: Optional[str] = None
    source_link: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


class KnowledgeDB(AsyncAttrs, SQLModel, table=True):
    __tablename__ = "knowledge"  # type: ignore

    id: UUID | None = Field(
        default=None,
        sa_column=Column(
            PGUUID,
            server_default=text("uuid_generate_v4()"),
            primary_key=True,
        ),
    )
    file_name: Optional[str] = Field(default=None, max_length=255)
    url: Optional[str] = Field(default=None, max_length=2048)
    extension: str = Field(default=".txt", max_length=100)
    status: str = Field(max_length=50)
    source: str = Field(max_length=255)
    source_link: Optional[str] = Field(max_length=2048)
    file_size: Optional[int] = Field(gt=0)  # FIXME: Should not be optional @chloedia
    file_sha1: Optional[str] = Field(
        max_length=40
    )  # FIXME: Should not be optional @chloedia
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=False),
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=False),
            server_default=text("CURRENT_TIMESTAMP"),
            onupdate=datetime.utcnow,
        ),
    )
    metadata_: Optional[Dict[str, str]] = Field(
        default=None, sa_column=Column("metadata", JSON)
    )
    is_folder: bool = Field(default=False)
    user_id: UUID = Field(foreign_key="users.id", nullable=False)
    brains: List["Brain"] = Relationship(
        back_populates="knowledges",
        link_model=KnowledgeBrain,
        sa_relationship_kwargs={"lazy": "select"},
    )

    parent_id: UUID | None = Field(
        default=None, foreign_key="knowledge.id", ondelete="CASCADE"
    )
    parent: Optional["KnowledgeDB"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "KnowledgeDB.id"},
    )
    children: list["KnowledgeDB"] = Relationship(
        back_populates="parent",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
        },
    )

    # TODO: nested folder search
    async def to_dto(self, get_children: bool = True) -> Knowledge:
        assert (
            self.updated_at
        ), "knowledge should be inserted before transforming to dto"
        assert (
            self.created_at
        ), "knowledge should be inserted before transforming to dto"
        brains = await self.awaitable_attrs.brains
        children: list[KnowledgeDB] = (
            await self.awaitable_attrs.children if get_children else []
        )
        parent = await self.awaitable_attrs.parent
        parent = await parent.to_dto(get_children=False) if parent else None

        return Knowledge(
            id=self.id,  # type: ignore
            file_name=self.file_name,
            url=self.url,
            extension=self.extension,
            status=KnowledgeStatus(self.status),
            source=self.source,
            source_link=self.source_link,
            is_folder=self.is_folder,
            file_size=self.file_size or 0,
            file_sha1=self.file_sha1,
            updated_at=self.updated_at,
            created_at=self.created_at,
            metadata=self.metadata_,  # type: ignore
            brains=[b.model_dump() for b in brains],
            parent=parent,
            children=[await c.to_dto(get_children=False) for c in children],
            user_id=self.user_id,
        )
