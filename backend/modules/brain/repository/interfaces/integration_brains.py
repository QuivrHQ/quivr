from abc import ABC, abstractmethod
from uuid import UUID

from modules.brain.entity.integration_brain import IntegrationBrainEntity


class IntegrationBrain(ABC):
    @abstractmethod
    def get_integration_brain(self, brain_id: UUID) -> IntegrationBrainEntity:
        """Get the integration brain entity

        Args:
            brain_id (UUID): ID of the brain

        Returns:
            IntegrationBrainEntity: Integration brain entity
        """
        pass

    @abstractmethod
    def add_integration_brain(
        self, brain_id: UUID, integration_brain: IntegrationBrainEntity
    ) -> IntegrationBrainEntity:
        pass

    @abstractmethod
    def update_integration_brain(
        self, brain_id: UUID, integration_brain: IntegrationBrainEntity
    ) -> IntegrationBrainEntity:
        pass

    @abstractmethod
    def delete_integration_brain(self, brain_id: UUID) -> None:
        pass
