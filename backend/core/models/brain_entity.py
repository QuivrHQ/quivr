from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from routes.authorizations.types import RoleEnum


class BrainEntity(BaseModel):
    brain_id: UUID
    name: str
    description: Optional[str]
    temperature: Optional[float]
    model: Optional[str]
    max_tokens: Optional[int]
    openai_api_key: Optional[str]
    status: Optional[str]
    prompt_id: Optional[UUID]


class MinimalBrainEntity(BaseModel):
    id: UUID
    name: str
    rights: RoleEnum
