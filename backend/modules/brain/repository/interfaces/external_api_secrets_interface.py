from abc import ABC, abstractmethod
from uuid import UUID


class ExternalApiSecretsInterface(ABC):
    @abstractmethod
    def create_secret(
        self, user_id: UUID, brain_id: UUID, secret_name: str, secret_value
    ) -> UUID | None:
        """
        Create a new secret for the API Request in given brain
        """
        pass

    @abstractmethod
    def read_secret(
        self, user_id: UUID, brain_id: UUID, secret_name: str
    ) -> UUID | None:
        """
        Read a secret for the API Request in given brain
        """
        pass

    @abstractmethod
    def delete_secret(self, user_id: UUID, brain_id: UUID, secret_name: str) -> bool:
        """
        Delete a secret from a brain
        """
        pass
