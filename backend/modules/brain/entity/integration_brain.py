from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class IntegrationDescriptionEntity(BaseModel):
    id: UUID
    integration_name: str
    integration_logo_url: Optional[str]
    connection_settings: Optional[dict]


class IntegrationEntity(BaseModel):
    id: UUID
    user_id: UUID
    brain_id: UUID
    integration_id: str
    settings: Optional[dict]
    credentials: Optional[dict]
