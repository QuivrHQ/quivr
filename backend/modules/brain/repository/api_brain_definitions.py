from typing import Optional
from uuid import UUID

from models.settings import get_supabase_client
from modules.brain.dto.inputs import CreateApiBrainDefinition
from modules.brain.entity.api_brain_definition_entity import ApiBrainDefinitionEntity
from modules.brain.repository.interfaces import ApiBrainDefinitionsInterface


class ApiBrainDefinitions(ApiBrainDefinitionsInterface):
    def __init__(self):
        self.db = get_supabase_client()

    def get_api_brain_definition(
        self, brain_id: UUID
    ) -> Optional[ApiBrainDefinitionEntity]:
        response = (
            self.db.table("api_brain_definition")
            .select("*")
            .filter("brain_id", "eq", brain_id)
            .execute()
        )
        if len(response.data) == 0:
            return None

        return ApiBrainDefinitionEntity(**response.data[0])

    def add_api_brain_definition(
        self, brain_id: UUID, api_brain_definition: CreateApiBrainDefinition
    ) -> Optional[ApiBrainDefinitionEntity]:
        response = (
            self.db.table("api_brain_definition")
            .insert([{"brain_id": str(brain_id), **api_brain_definition.dict()}])
            .execute()
        )
        if len(response.data) == 0:
            return None
        return ApiBrainDefinitionEntity(**response.data[0])

    def update_api_brain_definition(
        self, brain_id: UUID, api_brain_definition: ApiBrainDefinitionEntity
    ) -> Optional[ApiBrainDefinitionEntity]:
        response = (
            self.db.table("api_brain_definition")
            .update(api_brain_definition.dict(exclude={"brain_id"}))
            .filter("brain_id", "eq", str(brain_id))
            .execute()
        )
        if len(response.data) == 0:
            return None
        return ApiBrainDefinitionEntity(**response.data[0])

    def delete_api_brain_definition(self, brain_id: UUID) -> None:
        self.db.table("api_brain_definition").delete().filter(
            "brain_id", "eq", str(brain_id)
        ).execute()
