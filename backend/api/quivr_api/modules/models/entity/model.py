from sqlmodel import Field, SQLModel


class Model(SQLModel, table=True):  # type: ignore
    __tablename__ = "models"  # type: ignore

    name: str = Field(primary_key=True)
    price: int = Field(default=1)
    max_input: int = Field(default=2000)
    max_output: int = Field(default=1000)
    description: str = Field(default="")
    display_name: str = Field(default="")
    image_url: str = Field(default="")
    endpoint_url: str = Field(default="")
    env_variable_name: str = Field(default="")
    default: bool = Field(default=False)

    class Config:
        arbitrary_types_allowed = True
