from uuid import UUID

from pydantic import BaseModel


class CompositeBrainConnectionEntity(BaseModel):
    composite_brain_id: UUID
    connected_brain_id: UUID
