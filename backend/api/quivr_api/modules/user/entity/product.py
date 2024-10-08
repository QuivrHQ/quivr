from typing import List

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


class ProductSettings(SQLModel, table=True):
    __tablename__ = "product_to_features"  # type: ignore

    id: int | None = Field(
        primary_key=True,
        nullable=False,
    )
    # FIXME(@StanGirard): should be an array
    models: List[str] = Field(sa_column=Column("models", JSON))
    max_brains: int
    max_brain_size: int
    stripe_product_id: str
    api_access: bool
    monthly_chat_credit: int
    max_storage: int
    # users: List["User"] | None = Relationship(back_populates="product")  # type: ignore # noqa: F821
