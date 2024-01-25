from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Extra


class ApiBrainDefinitionSchemaProperty(BaseModel, extra=Extra.forbid):
    type: str
    description: str
    enum: Optional[list]
    name: str

    def dict(self, **kwargs):
        result = super().dict(**kwargs)
        if "enum" in result and result["enum"] is None:
            del result["enum"]
        return result


class ApiBrainDefinitionSchema(BaseModel, extra=Extra.forbid):
    properties: list[ApiBrainDefinitionSchemaProperty] = []
    required: list[str] = []


class ApiBrainDefinitionSecret(BaseModel, extra=Extra.forbid):
    name: str
    type: str
    description: Optional[str]


class ApiBrainAllowedMethods(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class ApiBrainDefinitionEntity(BaseModel, extra=Extra.forbid):
    brain_id: UUID
    method: ApiBrainAllowedMethods
    url: str
    params: ApiBrainDefinitionSchema
    search_params: ApiBrainDefinitionSchema
    secrets: list[ApiBrainDefinitionSecret]
    raw: bool = False
    jq_instructions: Optional[str] = None
