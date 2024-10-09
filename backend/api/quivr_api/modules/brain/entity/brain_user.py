from uuid import UUID

from sqlmodel import Field, SQLModel


class BrainUserDB(SQLModel, table=True):
    __tablename__ = "brains_users"  # type: ignore

    brain_id: UUID = Field(
        nullable=False, foreign_key="brains.brain_id", primary_key=True
    )
    user_id: UUID = Field(nullable=False, foreign_key="users.id", primary_key=True)
    default_brain: bool
    rights: str
