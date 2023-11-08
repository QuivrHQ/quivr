from uuid import UUID

from pydantic import BaseModel


class ApiBrainDefinition(BaseModel):
    brain_id: UUID
    method: str
    url: str
    params: dict
    search_params: dict
    secrets: dict
