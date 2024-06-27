from uuid import UUID

from pydantic import BaseModel


class AssistantEntity(BaseModel):
    id: UUID
    name: str
    brain_id_required: bool
    file_1_required: bool
    url_required: bool
