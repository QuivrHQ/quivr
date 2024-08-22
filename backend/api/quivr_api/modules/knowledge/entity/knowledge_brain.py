from datetime import datetime
from uuid import UUID

from sqlalchemy import TIMESTAMP, Column, text
from sqlmodel import TIMESTAMP, Column, Field, Relationship, SQLModel, text
from sqlmodel import UUID as PGUUID


class KnowledgeBrain(SQLModel, table=True):
    __tablename__ = "knowledge_brain"  # type: ignore

    id: UUID | None = Field(
        default=None,
        sa_column=Column(
            PGUUID,
            server_default=text("uuid_generate_v4()"),
            primary_key=True,
        ),
    )
    created_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=False),
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    brain_id: UUID = Field(nullable=False, foreign_key="brains.brain_id")
    knowledge_id: UUID = Field(nullable=False, foreign_key="knowledge.id")

    knowledge: "KnowledgeDB" = Relationship(back_populates="knowledge_brain")

    brain: "Brain" = Relationship(back_populates="knowledge_brain")

    # knowledge: KnowledgeDB| None = Relationship(back_populates="knowledge_brain")  # type: ignore
    # brain: Brain | None = Relationship(back_populates="knowledge_brain")  # type: ignore
