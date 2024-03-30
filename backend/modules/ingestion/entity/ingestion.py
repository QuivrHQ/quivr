from uuid import UUID

from pydantic import BaseModel


class IngestionEntity(BaseModel):
    id: UUID
    name: str
