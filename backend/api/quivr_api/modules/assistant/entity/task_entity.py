from datetime import datetime
from uuid import UUID

from sqlmodel import TIMESTAMP, Column, Field, SQLModel, text, JSON, BigInteger
from typing import Dict

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
    # Json for answer_raw
    answer_raw: Dict = Field(default_factory=dict, sa_column=Column(JSON))
    answer_pretty: str | None = Field(default=None)
    
    class Config:
        arbitrary_types_allowed = True
