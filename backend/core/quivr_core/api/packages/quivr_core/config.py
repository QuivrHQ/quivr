from pydantic import BaseModel, field_validator


class RAGConfig(BaseModel):
    model: str = "gpt-3.5-turbo-0125"  # pyright: ignore reportPrivateUsage=none
    temperature: float | None = 0.1
    max_tokens: int | None = 2000
    max_input: int = 2000
    streaming: bool = False
    max_files: int = 20
    prompt: str | None = None

    @field_validator("temperature", mode="before")
    def set_default_temperature(cls, v):
        if v is None:
            return 0.1
        return v

    @field_validator("max_tokens", mode="before")
    def set_default_max_tokens(cls, v):
        if v is None:
            return 2000
        return v
