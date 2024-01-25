from enum import Enum
from typing import List, Optional
from uuid import UUID

from modules.brain.entity.api_brain_definition_entity import ApiBrainDefinitionEntity
from pydantic import BaseModel


class BrainType(str, Enum):
    DOC = "doc"
    API = "api"
    COMPOSITE = "composite"


class BrainEntity(BaseModel):
    brain_id: UUID
    name: str
    description: Optional[str]
    temperature: Optional[float]
    model: Optional[str]
    max_tokens: Optional[int]
    status: Optional[str]
    prompt_id: Optional[UUID]
    last_update: str
    brain_type: BrainType
    brain_definition: Optional[ApiBrainDefinitionEntity]
    connected_brains_ids: Optional[List[UUID]]
    raw: Optional[bool]
    jq_instructions: Optional[str]

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
    description: Optional[str]
    number_of_subscribers: int = 0
    last_update: str
    brain_type: BrainType
    brain_definition: Optional[ApiBrainDefinitionEntity]


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
