from abc import ABC, abstractmethod
from uuid import UUID

from quivr_api.modules.brain.dto.inputs import (
    BrainUpdatableProperties,
    CreateBrainProperties,
)
from quivr_api.modules.brain.entity.brain_entity import BrainEntity, PublicBrain


class BrainsInterface(ABC):
    @abstractmethod
    def create_brain(self, brain: CreateBrainProperties) -> BrainEntity:
        """
        Create a brain in the brains table
        """
        pass

    @abstractmethod
    def get_public_brains(self) -> list[PublicBrain]:
        """
        Get all public brains
        """
        pass

    @abstractmethod
    def get_brain_details(self, brain_id: UUID, user_id: UUID) -> BrainEntity | None:
        """
        Get all public brains
        """
        pass

    @abstractmethod
    def update_brain_last_update_time(self, brain_id: UUID) -> None:
        """
        Update the last update time of the brain
        """
        pass

    @abstractmethod
    def delete_brain(self, brain_id: UUID):
        """
        Delete a brain
        """
        pass

    @abstractmethod
    def update_brain_by_id(
        self, brain_id: UUID, brain: BrainUpdatableProperties
    ) -> BrainEntity | None:
        """
        Update a brain by id
        """
        pass

    @abstractmethod
    def get_brain_by_id(self, brain_id: UUID) -> BrainEntity | None:
        """
        Get a brain by id
        """
        pass
