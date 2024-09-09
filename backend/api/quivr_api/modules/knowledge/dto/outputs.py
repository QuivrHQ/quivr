from uuid import UUID

from pydantic import BaseModel


class DeleteKnowledgeResponse(BaseModel):
    file_name: str | None = None
    status: str = "delete"
    knowledge_id: UUID
