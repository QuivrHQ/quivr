from abc import ABC, abstractmethod
from uuid import UUID

from modules.user.dto.inputs import UserUpdatableProperties
from modules.user.entity.user_identity import UserIdentity


class UsersInterface(ABC):
    @abstractmethod
    def create_user_identity(self, id: UUID) -> UserIdentity:
        """
        Create a user identity
        """
        pass

    @abstractmethod
    def update_user_properties(
        self,
        user_id: UUID,
        user_identity_updatable_properties: UserUpdatableProperties,
    ) -> UserIdentity:
        """
        Update the user properties
        """
        pass

    @abstractmethod
    def get_user_identity(self, user_id: UUID) -> UserIdentity:
        """
        Get the user identity
        """
        pass

    @abstractmethod
    def get_user_id_by_user_email(self, email: str) -> UUID | None:
        """
        Get the user id by user email
        """
        pass

    @abstractmethod
    def get_user_email_by_user_id(self, user_id: UUID) -> str:
        """
        Get the user email by user id
        """
        pass
