from abc import ABC, abstractmethod
from uuid import UUID

from modules.brain.entity.integration_brain import (
    IntegrationDescriptionEntity,
    IntegrationEntity,
)


class IntegrationBrainInterface(ABC):
    @abstractmethod
    def get_integration_brain(self, brain_id: UUID, user_id: UUID) -> IntegrationEntity:
        """Get the integration brain entity

        Args:
            brain_id (UUID): ID of the brain

        Returns:
            IntegrationEntity: Integration brain entity
        """
        pass

    @abstractmethod
    def add_integration_brain(
        self, brain_id: UUID, integration_brain: IntegrationEntity
    ) -> IntegrationEntity:
        pass

    @abstractmethod
    def update_integration_brain(
        self, brain_id: UUID, integration_brain: IntegrationEntity
    ) -> IntegrationEntity:
        pass

    @abstractmethod
    def delete_integration_brain(self, brain_id: UUID) -> None:
        pass


class IntegrationDescriptionInterface(ABC):

    @abstractmethod
    def get_integration_description(
        self, integration_id: UUID
    ) -> IntegrationDescriptionEntity:
        """Get the integration description entity

        Args:
            integration_id (UUID): ID of the integration

        Returns:
            IntegrationEntity: Integration description entity
        """
        pass

    @abstractmethod
    def get_all_integration_descriptions(self) -> list[IntegrationDescriptionEntity]:
        pass

    @abstractmethod
    def get_integration_description_by_user_brain_id(
        self, brain_id: UUID, user_id: UUID
    ) -> IntegrationDescriptionEntity:
        pass
