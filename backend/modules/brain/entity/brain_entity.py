from enum import Enum
from typing import List, Optional
from uuid import UUID

from modules.brain.entity.api_brain_definition_entity import ApiBrainDefinitionEntity
from modules.brain.entity.integration_brain import (
    IntegrationDescriptionEntity,
    IntegrationEntity,
)
from pydantic import BaseModel


class BrainType(str, Enum):
    DOC = "doc"
    API = "api"
    COMPOSITE = "composite"
    INTEGRATION = "integration"


class BrainEntity(BaseModel):
    brain_id: UUID
    name: str
    description: Optional[str] = None
    temperature: Optional[float] = None
    model: Optional[str] = None
    max_tokens: Optional[int] = None
    status: Optional[str] = None
    prompt_id: Optional[UUID] = None
    last_update: str
    brain_type: BrainType
    brain_definition: Optional[ApiBrainDefinitionEntity] = None
    connected_brains_ids: Optional[List[UUID]] = None
    raw: Optional[bool] = None
    jq_instructions: Optional[str] = None
    integration: Optional[IntegrationEntity] = None
    integration_description: Optional[IntegrationDescriptionEntity] = None

    @property
    def id(self) -> UUID:
        return self.brain_id

    def dict(self, **kwargs):
        data = super().dict(
            **kwargs,
        )
        data["id"] = self.id
        return data


class PublicBrain(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    number_of_subscribers: int = 0
    last_update: str
    brain_type: BrainType
    brain_definition: Optional[ApiBrainDefinitionEntity] = None


class RoleEnum(str, Enum):
    Viewer = "Viewer"
    Editor = "Editor"
    Owner = "Owner"


class BrainUser(BaseModel):
    id: UUID
    user_id: UUID
    rights: RoleEnum
    default_brain: bool = False


class MinimalUserBrainEntity(BaseModel):
    id: UUID
    name: str
    rights: RoleEnum
    status: str
    brain_type: BrainType
    description: str
    integration_logo_url: str
    max_files: int
