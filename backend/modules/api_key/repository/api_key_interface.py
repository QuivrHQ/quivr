from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from modules.api_key.entity.api_key import ApiKey


class ApiKeysInterface(ABC):
    @abstractmethod
    def create_api_key(
        self,
        new_key_id: UUID,
        new_api_key: str,
        user_id: UUID,
        days: int,
        only_chat: bool,
    ):
        pass

    @abstractmethod
    def delete_api_key(self, key_id: UUID, user_id: UUID):
        pass

    @abstractmethod
    def get_active_api_key(self, api_key: UUID):
        pass

    @abstractmethod
    def get_user_id_by_api_key(self, api_key: UUID):
        pass

    @abstractmethod
    def get_user_api_keys(self, user_id: UUID) -> List[ApiKey]:
        pass
