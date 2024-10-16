import asyncio
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import UUID

from quivr_core.models import KnowledgeStatus
from sqlalchemy import JSON, TIMESTAMP, Column, text
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlmodel import UUID as PGUUID
from sqlmodel import Field, Relationship, SQLModel

from quivr_api.modules.knowledge.dto.outputs import KnowledgeDTO, sort_knowledge_dtos
from quivr_api.modules.knowledge.entity.knowledge_brain import KnowledgeBrain
from quivr_api.modules.sync.entity.sync_models import Sync


class KnowledgeSource(str, Enum):
    LOCAL = "local"
    WEB = "web"
    NOTETAKER = "notetaker"
    GOOGLE = "google"
    AZURE = "azure"
    DROPBOX = "dropbox"
    NOTION = "notion"
    GITHUB = "github"


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
            TIMESTAMP(timezone=True),
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True),
            server_default=text("CURRENT_TIMESTAMP"),
            onupdate=datetime.utcnow,
        ),
    )

    last_synced_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True),
        ),
    )
    metadata_: Optional[Dict[str, str]] = Field(
        default=None, sa_column=Column("metadata", JSON)
    )
    is_folder: bool = Field(default=False)
    user_id: UUID = Field(foreign_key="users.id", nullable=False)
    brains: List["Brain"] = Relationship(  # type: ignore # noqa: F821
        back_populates="knowledges",
        link_model=KnowledgeBrain,
        sa_relationship_kwargs={"lazy": "joined"},
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
    sync_id: int | None = Field(
        default=None, foreign_key="syncs.id", ondelete="CASCADE"
    )
    sync: Sync | None = Relationship(
        back_populates="knowledges", sa_relationship_kwargs={"lazy": "joined"}
    )
    sync_file_id: str | None = Field(default=None)

    # TODO: nested folder search
    async def to_dto(
        self, get_children: bool = True, get_parent: bool = True
    ) -> KnowledgeDTO:
        assert (
            await self.awaitable_attrs.updated_at
        ), "knowledge should be inserted before transforming to dto"
        assert (
            await self.awaitable_attrs.created_at
        ), "knowledge should be inserted before transforming to dto"
        brains = await self.awaitable_attrs.brains
        brains = sorted(brains, key=lambda b: (b is None, b.name))
        children: list[KnowledgeDB] = (
            await self.awaitable_attrs.children if get_children else []
        )
        children_dto = await asyncio.gather(
            *[c.to_dto(get_children=False) for c in children]
        )
        children_dto = sort_knowledge_dtos(children_dto)
        parent = await self.awaitable_attrs.parent if get_parent else None
        parent_dto = await parent.to_dto(get_children=False) if parent else None

        return KnowledgeDTO(
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
            updated_at=await self.awaitable_attrs.updated_at,
            created_at=await self.awaitable_attrs.created_at,
            metadata=self.metadata_,  # type: ignore
            brains=[b.model_dump() for b in brains],
            parent=parent_dto,
            children=children_dto,
            user_id=self.user_id,
            sync_id=self.sync_id,
            sync_file_id=self.sync_file_id,
            last_synced_at=self.last_synced_at,
        )
