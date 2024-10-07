from pydantic import BaseModel


class LLMModel(BaseModel):
    """LLM models stored in the database that are allowed to be used by the users.
    Args:
        BaseModel (BaseModel): Pydantic BaseModel
    """

    name: str = "gpt-4o"
    price: int = 1
    max_context_tokens: int = 512
    max_output_tokens: int = 512
