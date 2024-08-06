from sqlmodel import Field, SQLModel


class Model(SQLModel, table=True):
    __tablename__ = "models"

    name: str = Field(primary_key=True)
    price: int = Field(default=1)
    max_input: int = Field(default=2000)
    max_output: int = Field(default=1000)

    class Config:
        arbitrary_types_allowed = True
