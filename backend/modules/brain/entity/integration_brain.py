from typing import Optional
from uuid import UUID

from modules.brain.dto.inputs import IntegrationType
from pydantic import BaseModel


class IntegrationDescriptionEntity(BaseModel):
    id: UUID
    integration_name: str
    integration_logo_url: Optional[str] = None
    connection_settings: Optional[dict] = None
    integration_type: IntegrationType
    description: str
    max_files: int


class IntegrationEntity(BaseModel):
    id: int
    user_id: str
    brain_id: str
    integration_id: str
    settings: Optional[dict] = None
    credentials: Optional[dict] = None
