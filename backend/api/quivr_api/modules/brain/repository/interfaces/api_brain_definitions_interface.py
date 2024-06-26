from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from quivr_api.modules.brain.dto.inputs import CreateApiBrainDefinition
from quivr_api.modules.brain.entity.api_brain_definition_entity import (
    ApiBrainDefinitionEntity,
)


class ApiBrainDefinitionsInterface(ABC):
    @abstractmethod
    def get_api_brain_definition(
        self, brain_id: UUID
    ) -> Optional[ApiBrainDefinitionEntity]:
        pass

    @abstractmethod
    def add_api_brain_definition(
        self, brain_id: UUID, api_brain_definition: CreateApiBrainDefinition
    ) -> Optional[ApiBrainDefinitionEntity]:
        pass

    @abstractmethod
    def update_api_brain_definition(
        self, brain_id: UUID, api_brain_definition: ApiBrainDefinitionEntity
    ) -> Optional[ApiBrainDefinitionEntity]:
        """
        Get all public brains
        """
        pass

    @abstractmethod
    def delete_api_brain_definition(self, brain_id: UUID) -> None:
        """
        Update the last update time of the brain
        """
        pass
