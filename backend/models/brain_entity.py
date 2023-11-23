from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from routes.authorizations.types import RoleEnum

from models.ApiBrainDefinition import ApiBrainDefinition


class BrainType(str, Enum):
    DOC = "doc"
    API = "api"


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
    brain_definition: Optional[ApiBrainDefinition]

    @property
    def id(self) -> UUID:
        return self.brain_id

    def dict(self, **kwargs):
        data = super().dict(
            **kwargs,
        )
        data["id"] = self.id
        return data


class MinimalBrainEntity(BaseModel):
    id: UUID
    name: str
    rights: RoleEnum
    status: str
    brain_type: BrainType


class PublicBrain(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    number_of_subscribers: int = 0
    last_update: str
    brain_type: BrainType
    brain_definition: Optional[ApiBrainDefinition]


class BrainUser(BaseModel):
    id: UUID
    user_id: UUID
    rights: RoleEnum
    default_brain: bool = False
