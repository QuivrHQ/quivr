from abc import ABC, abstractmethod
from uuid import UUID

from modules.sync.dto.inputs import SyncsUserInput, SyncUserUpdateInput


class SyncInterface(ABC):
    @abstractmethod
    def create_sync_user(
        self,
        sync_user_input: SyncsUserInput,
    ):
        pass

    @abstractmethod
    def get_syncs_user(self, user_id: UUID):
        pass

    @abstractmethod
    def delete_sync_user(self, sync_user_id: UUID, user_id: UUID):
        pass

    @abstractmethod
    def get_sync_user_by_state(self, state: dict):
        pass

    @abstractmethod
    def update_sync_user(
        self, sync_user_id: str, state: dict, sync_user_input: SyncUserUpdateInput
    ):
        pass
