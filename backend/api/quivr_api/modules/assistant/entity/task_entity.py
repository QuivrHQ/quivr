from datetime import datetime
from uuid import UUID

from sqlmodel import TIMESTAMP, Column, Field, SQLModel, text
from sqlmodel import UUID as PGUUID


class Task(SQLModel, table=True):
    __tablename__ = "tasks"  # type: ignore

    id: UUID | None = Field(
        default=None,
        sa_column=Column(
            PGUUID,
            server_default=text("uuid_generate_v4()"),
            primary_key=True,
        ),
    )

    pretty_id: str
    user_id: UUID = Field(foreign_key="users.id")
    status: str
    creation_time: datetime | None = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=False),
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    # Json for answer_raw
    answer_raw: dict | None = Field(default=None)
    answer_pretty: str | None = Field(default=None)
