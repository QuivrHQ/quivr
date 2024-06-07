from uuid import UUID

from sqlmodel import Field, SQLModel


class BaseUUIDModel(SQLModel):
    id: UUID = Field(
        primary_key=True,
        index=True,
        nullable=False,
    )
