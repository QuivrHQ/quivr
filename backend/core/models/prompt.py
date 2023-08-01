from uuid import UUID

from pydantic import BaseModel


class Prompt(BaseModel):
    title: str
    content: str
    status: str = "private"
    id: UUID
