from pydantic import BaseModel


class UserUpdatableProperties(BaseModel):
    # Nothing for now
    empty: bool = True
