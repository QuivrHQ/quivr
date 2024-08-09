from uuid import UUID

from pydantic import BaseModel


class CreateVectorType(BaseModel):
    content: str
    metadata_: dict
    knowledge_id: UUID
