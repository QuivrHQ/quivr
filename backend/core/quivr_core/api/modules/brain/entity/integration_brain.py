from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class IntegrationType(str, Enum):
    CUSTOM = "custom"
    SYNC = "sync"
    DOC = "doc"


class IntegrationBrainTag(str, Enum):
    NEW = "new"
    RECOMMENDED = "recommended"
    MOST_POPULAR = "most_popular"
    PREMIUM = "premium"
    COMING_SOON = "coming_soon"
    COMMUNITY = "community"
    DEPRECATED = "deprecated"


class IntegrationDescriptionEntity(BaseModel):
    id: UUID
    integration_name: str
    integration_logo_url: Optional[str] = None
    connection_settings: Optional[dict] = None
    integration_type: IntegrationType
    tags: Optional[list[IntegrationBrainTag]] = []
    information: Optional[str] = None
    description: str
    max_files: int
    allow_model_change: bool
    integration_display_name: str
    onboarding_brain: bool


class IntegrationEntity(BaseModel):
    id: int
    user_id: str
    brain_id: str
    integration_id: str
    settings: Optional[dict] = None
    credentials: Optional[dict] = None
    last_synced: str
