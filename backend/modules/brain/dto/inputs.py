from typing import Optional
from uuid import UUID

from logger import get_logger
from modules.brain.entity.api_brain_definition_entity import (
    ApiBrainAllowedMethods,
    ApiBrainDefinitionEntity,
    ApiBrainDefinitionSchema,
    ApiBrainDefinitionSecret,
)
from modules.brain.entity.brain_entity import BrainType
from pydantic import BaseModel, Extra

logger = get_logger(__name__)


class CreateApiBrainDefinition(BaseModel, extra=Extra.forbid):
    method: ApiBrainAllowedMethods
    url: str
    params: Optional[ApiBrainDefinitionSchema] = ApiBrainDefinitionSchema()
    search_params: ApiBrainDefinitionSchema = ApiBrainDefinitionSchema()
    secrets: Optional[list[ApiBrainDefinitionSecret]] = []
    raw: Optional[bool] = False
    jq_instructions: Optional[str] = None


class CreateBrainProperties(BaseModel, extra=Extra.forbid):
    name: Optional[str] = "Default brain"
    description: str = "This is a description"
    status: Optional[str] = "private"
    model: Optional[str]
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = 2000
    prompt_id: Optional[UUID] = None
    brain_type: Optional[BrainType] = BrainType.DOC
    brain_definition: Optional[CreateApiBrainDefinition]
    brain_secrets_values: dict = {}
    connected_brains_ids: Optional[list[UUID]] = []

    def dict(self, *args, **kwargs):
        brain_dict = super().dict(*args, **kwargs)
        if brain_dict.get("prompt_id"):
            brain_dict["prompt_id"] = str(brain_dict.get("prompt_id"))
        return brain_dict


class BrainUpdatableProperties(BaseModel):
    name: Optional[str]
    description: Optional[str]
    temperature: Optional[float]
    model: Optional[str]
    max_tokens: Optional[int]
    status: Optional[str]
    prompt_id: Optional[UUID]
    brain_definition: Optional[ApiBrainDefinitionEntity]
    connected_brains_ids: Optional[list[UUID]] = []

    def dict(self, *args, **kwargs):
        brain_dict = super().dict(*args, **kwargs)
        if brain_dict.get("prompt_id"):
            brain_dict["prompt_id"] = str(brain_dict.get("prompt_id"))
        return brain_dict


class BrainQuestionRequest(BaseModel):
    question: str
