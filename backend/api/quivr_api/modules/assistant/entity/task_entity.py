from datetime import datetime
from typing import Dict
from uuid import UUID

from sqlmodel import JSON, TIMESTAMP, BigInteger, Column, Field, SQLModel, text


class Task(SQLModel, table=True):
    __tablename__ = "tasks"  # type: ignore

    id: int | None = Field(
        default=None,
        sa_column=Column(
            BigInteger,
            primary_key=True,
            autoincrement=True,
        ),
    )
    assistant_id: int
    pretty_id: str
    user_id: UUID
    status: str = Field(default="pending")
    creation_time: datetime | None = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=False),
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    settings: Dict = Field(default_factory=dict, sa_column=Column(JSON))
    answer: str | None = Field(default=None)

    class Config:
        arbitrary_types_allowed = True
