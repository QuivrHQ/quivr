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
from modules.brain.entity.integration_brain import IntegrationType
from pydantic import BaseModel, Extra

logger = get_logger(__name__)


class CreateApiBrainDefinition(BaseModel, extra="ignore"):
    method: ApiBrainAllowedMethods
    url: str
    params: Optional[ApiBrainDefinitionSchema] = ApiBrainDefinitionSchema()
    search_params: ApiBrainDefinitionSchema = ApiBrainDefinitionSchema()
    secrets: Optional[list[ApiBrainDefinitionSecret]] = []
    raw: Optional[bool] = False
    jq_instructions: Optional[str] = None


class CreateIntegrationBrain(BaseModel, extra="ignore"):
    integration_name: str
    integration_logo_url: str
    connection_settings: dict
    integration_type: IntegrationType
    description: str
    max_files: int


class BrainIntegrationSettings(BaseModel, extra="ignore"):
    integration_id: str
    settings: dict


class BrainIntegrationUpdateSettings(BaseModel, extra="ignore"):
    settings: dict


class CreateBrainProperties(BaseModel, extra="ignore"):
    name: Optional[str] = "Default brain"
    description: str = "This is a description"
    status: Optional[str] = "private"
    model: Optional[str] = None
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = 2000
    prompt_id: Optional[UUID] = None
    brain_type: Optional[BrainType] = BrainType.DOC
    brain_definition: Optional[CreateApiBrainDefinition] = None
    brain_secrets_values: Optional[dict] = {}
    connected_brains_ids: Optional[list[UUID]] = []
    integration: Optional[BrainIntegrationSettings] = None

    def dict(self, *args, **kwargs):
        brain_dict = super().dict(*args, **kwargs)
        if brain_dict.get("prompt_id"):
            brain_dict["prompt_id"] = str(brain_dict.get("prompt_id"))
        return brain_dict


class BrainUpdatableProperties(BaseModel, extra="ignore"):

    name: Optional[str] = None
    description: Optional[str] = None
    temperature: Optional[float] = None
    model: Optional[str] = None
    max_tokens: Optional[int] = None
    status: Optional[str] = None
    prompt_id: Optional[UUID] = None
    brain_definition: Optional[ApiBrainDefinitionEntity] = None
    connected_brains_ids: Optional[list[UUID]] = []
    integration: Optional[BrainIntegrationUpdateSettings] = None

    def dict(self, *args, **kwargs):
        brain_dict = super().dict(*args, **kwargs)
        if brain_dict.get("prompt_id"):
            brain_dict["prompt_id"] = str(brain_dict.get("prompt_id"))
        return brain_dict


class BrainQuestionRequest(BaseModel):
    question: str
