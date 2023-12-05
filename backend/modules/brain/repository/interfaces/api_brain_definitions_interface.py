from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from modules.brain.dto.inputs import CreateApiBrainDefinition
from modules.brain.entity.api_brain_definition_entity import ApiBrainDefinition


class ApiBrainDefinitionsInterface(ABC):
    @abstractmethod
    def get_api_brain_definition(self, brain_id: UUID) -> Optional[ApiBrainDefinition]:
        pass

    @abstractmethod
    def add_api_brain_definition(
        self, brain_id: UUID, api_brain_definition: CreateApiBrainDefinition
    ) -> Optional[ApiBrainDefinition]:
        pass

    @abstractmethod
    def update_api_brain_definition(
        self, brain_id: UUID, api_brain_definition: ApiBrainDefinition
    ) -> Optional[ApiBrainDefinition]:
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
