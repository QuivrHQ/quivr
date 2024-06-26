from uuid import UUID

from pydantic import BaseModel


class DeleteKnowledgeResponse(BaseModel):
    status: str = "delete"
    knowledge_id: UUID
