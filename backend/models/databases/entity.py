from pydantic import BaseModel


class Models(BaseModel):
    """LLM models stored in the database that are allowed to be used by the users.
    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """
    name: str = "gpt-3.5-turbo-1106"
    price: int = 1
    max_input: int = 512
    max_output: int = 512