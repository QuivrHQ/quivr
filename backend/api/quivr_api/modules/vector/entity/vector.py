from typing import Optional
from uuid import UUID

from pgvector.sqlalchemy import Vector as PGVector
from pydantic import BaseModel
from sqlalchemy import Column
from sqlmodel import JSON, Column, Field, SQLModel, text
from sqlmodel import UUID as PGUUID

from quivr_api.models.settings import settings


class Vector(SQLModel, table=True):
    __tablename__ = "vectors"  # type: ignore
    id: UUID | None = Field(
        default=None,
        sa_column=Column(
            PGUUID,
            server_default=text("uuid_generate_v4()"),
            primary_key=True,
        ),
    )
    content: str = Field(default=None)
    metadata_: dict = Field(default={}, sa_column=Column("metadata", JSON, default={}))
    embedding: Optional[PGVector] = Field(
        sa_column=Column(PGVector(settings.embedding_dim)),
    )  # Verify with text_ada -> put it in Env variabme
    knowledge_id: UUID = Field(default=None, foreign_key="knowledge.id")

    class Config:
        arbitrary_types_allowed = True


class VectorType(BaseModel):
    id: UUID | None
    content: str
    metadata_: dict
    knowledge_id: UUID


class SimilaritySearchOutput(BaseModel):
    id: UUID
    brain_id: UUID
    knowledge_id: UUID
    content: str
    metadata_: dict
    embedding: str
    similarity: float
