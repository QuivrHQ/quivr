from abc import ABC, abstractmethod
from uuid import UUID

from modules.brain.entity.brain_entity import BrainUser, MinimalUserBrainEntity


class BrainsUsersInterface(ABC):
    @abstractmethod
    def get_user_brains(self, user_id) -> list[MinimalUserBrainEntity]:
        """
        Create a brain in the brains table
        """
        pass

    @abstractmethod
    def get_brain_for_user(self, user_id, brain_id) -> MinimalUserBrainEntity | None:
        """
        Get a brain for a user
        """
        pass

    @abstractmethod
    def delete_brain_user_by_id(
        self,
        user_id: UUID,
        brain_id: UUID,
    ):
        """
        Delete a user in a brain
        """
        pass

    @abstractmethod
    def delete_brain_users(self, brain_id: str):
        """
        Delete all users for a brain
        """
        pass

    @abstractmethod
    def create_brain_user(self, user_id: UUID, brain_id, rights, default_brain: bool):
        """
        Create a brain user
        """
        pass

    @abstractmethod
    def get_user_default_brain_id(self, user_id: UUID) -> UUID | None:
        """
        Get the default brain id for a user
        """
        pass

    @abstractmethod
    def get_brain_users(self, brain_id: UUID) -> list[BrainUser]:
        """
        Get all users for a brain
        """
        pass

    @abstractmethod
    def delete_brain_subscribers(self, brain_id: UUID):
        """
        Delete all subscribers for a brain with Viewer rights
        """
        pass

    @abstractmethod
    def get_brain_subscribers_count(self, brain_id: UUID) -> int:
        """
        Get the number of subscribers for a brain
        """
        pass
