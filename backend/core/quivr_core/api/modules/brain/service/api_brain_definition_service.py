from typing import Optional
from uuid import UUID

from quivr_core.api.modules.brain.dto.inputs import CreateApiBrainDefinition
from quivr_core.api.modules.brain.entity.api_brain_definition_entity import (
    ApiBrainDefinitionEntity,
)
from quivr_core.api.modules.brain.repository.api_brain_definitions import (
    ApiBrainDefinitions,
)


class ApiBrainDefinitionService:

    def __init__(self):
        self.repository = ApiBrainDefinitions()

    def add_api_brain_definition(
        self, brain_id: UUID, api_brain_definition: CreateApiBrainDefinition
    ) -> None:
        self.repository.add_api_brain_definition(brain_id, api_brain_definition)

    def delete_api_brain_definition(self, brain_id: UUID) -> None:
        self.repository.delete_api_brain_definition(brain_id)

    def get_api_brain_definition(
        self, brain_id: UUID
    ) -> Optional[ApiBrainDefinitionEntity]:
        return self.repository.get_api_brain_definition(brain_id)

    def update_api_brain_definition(
        self, brain_id: UUID, api_brain_definition: ApiBrainDefinitionEntity
    ) -> Optional[ApiBrainDefinitionEntity]:
        return self.repository.update_api_brain_definition(
            brain_id, api_brain_definition
        )
