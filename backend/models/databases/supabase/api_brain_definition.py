from enum import Enum
from typing import Optional
from uuid import UUID

from models.ApiBrainDefinition import (
    ApiBrainDefinition,
    ApiBrainDefinitionSchema,
    ApiBrainDefinitionSecret,
)
from models.databases.repository import Repository
from pydantic import BaseModel, Extra


class ApiMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class CreateApiBrainDefinition(BaseModel, extra=Extra.forbid):
    method: ApiMethod
    url: str
    params: Optional[ApiBrainDefinitionSchema] = ApiBrainDefinitionSchema()
    search_params: ApiBrainDefinitionSchema = ApiBrainDefinitionSchema()
    secrets: Optional[list[ApiBrainDefinitionSecret]] = []


class ApiBrainDefinitions(Repository):
    def __init__(self, supabase_client):
        self.db = supabase_client

    def get_api_brain_definition(self, brain_id: UUID) -> Optional[ApiBrainDefinition]:
        response = (
            self.db.table("api_brain_definition")
            .select("*")
            .filter("brain_id", "eq", brain_id)
            .execute()
        )
        if len(response.data) == 0:
            return None

        return ApiBrainDefinition(**response.data[0])

    def add_api_brain_definition(
        self, brain_id: UUID, api_brain_definition: CreateApiBrainDefinition
    ) -> Optional[ApiBrainDefinition]:
        response = (
            self.db.table("api_brain_definition")
            .insert([{"brain_id": str(brain_id), **api_brain_definition.dict()}])
            .execute()
        )
        if len(response.data) == 0:
            return None
        return ApiBrainDefinition(**response.data[0])

    def delete_api_brain_definition(self, brain_id: UUID) -> None:
        self.db.table("api_brain_definition").delete().filter(
            "brain_id", "eq", str(brain_id)
        ).execute()
