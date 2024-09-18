from uuid import UUID

from pydantic import BaseModel


class DeleteKnowledgeResponse(BaseModel):
    file_name: str | None = None
    status: str = "DELETED"
    knowledge_id: UUID
