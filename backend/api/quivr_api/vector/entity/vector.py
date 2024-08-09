from uuid import UUID

from pgvector.sqlalchemy import Vector as PGVector
from pydantic import BaseModel
from sqlalchemy import Column
from sqlmodel import JSON, Column, Field, SQLModel, text
from sqlmodel import UUID as PGUUID


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
    embedding: PGVector | None = Field(sa_column=Column(PGVector(256)))
    knowledge_id: UUID = Field(default=None, foreign_key="knowledge.id")


class VectorType(BaseModel):
    id: UUID | None
    content: str
    metadata_: dict
    embedding: PGVector | None
    knowledge_id: UUID
