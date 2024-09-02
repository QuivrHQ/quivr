from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel
from quivr_core.models import KnowledgeStatus
from sqlalchemy import JSON, TIMESTAMP, Column, text
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlmodel import UUID as PGUUID
from sqlmodel import Field, Relationship, SQLModel

from quivr_api.modules.knowledge.entity.knowledge_brain import KnowledgeBrain


class Knowledge(BaseModel):
    id: UUID
    file_name: Optional[str] = None
    url: Optional[str] = None
    extension: str = ".txt"
    status: str
    source: Optional[str] = None
    source_link: Optional[str] = None
    file_size: Optional[int] = None
    file_sha1: Optional[str] = None
    updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    metadata: Optional[Dict[str, str]] = None
    brain_ids: list[UUID]


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
    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=False),
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=False),
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    metadata_: Optional[Dict[str, str]] = Field(
        default=None, sa_column=Column("metadata", JSON)
    )
    user_id: UUID = Field(foreign_key="users.id", nullable=False)
    brains: List["Brain"] = Relationship(
        back_populates="knowledges",
        link_model=KnowledgeBrain,
        sa_relationship_kwargs={"lazy": "select"},
    )

    async def to_dto(self) -> Knowledge:
        brains = await self.awaitable_attrs.brains
        size = self.file_size if self.file_size else 0
        sha1 = self.file_sha1 if self.file_sha1 else ""
        return Knowledge(
            id=self.id,  # type: ignore
            file_name=self.file_name,
            url=self.url,
            extension=self.extension,
            status=KnowledgeStatus(self.status),
            source=self.source,
            source_link=self.source_link,
            file_size=size,
            file_sha1=sha1,
            updated_at=self.updated_at,
            created_at=self.created_at,
            metadata=self.metadata_,  # type: ignore
            brain_ids=[brain.brain_id for brain in brains],
        )
