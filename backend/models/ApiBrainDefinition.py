from uuid import UUID

from pydantic import BaseModel


class ApiBrainDefinitionSchemaProperty(BaseModel):
    type: str
    description: str
    enum: list
    name: str


class ApiBrainDefinitionSchema(BaseModel):
    properties: list[ApiBrainDefinitionSchemaProperty]
    required: list[str]


class ApiBrainDefinition(BaseModel):
    brain_id: UUID
    method: str
    url: str
    params: ApiBrainDefinitionSchema
    search_params: ApiBrainDefinitionSchema
    secrets: ApiBrainDefinitionSchema
