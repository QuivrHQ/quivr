from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel
from sqlmodel import JSON, TIMESTAMP, BigInteger, Column, Field, SQLModel, text


class TaskMetadata(BaseModel):
    input_files: Optional[List[str]] = None


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
    assistant_name: str
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
    task_metadata: Dict | None = Field(default_factory=dict, sa_column=Column(JSON))
