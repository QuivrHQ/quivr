from abc import ABC, abstractmethod
from uuid import UUID

from modules.sync.dto.inputs import SyncsUserInput, SyncUserUpdateInput
from modules.sync.dto.inputs import SyncsActiveInput, SyncsActiveUpdateInput
from modules.sync.entity.sync import SyncsActive

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
    
    @abstractmethod
    def create_sync_active(
        self,
        sync_active_input: SyncsActiveInput,
    ) -> SyncsActive:
        pass
    
    @abstractmethod
    def get_syncs_active(self, user_id: UUID) -> list[SyncsActive]:
        pass
    
    @abstractmethod
    def update_sync_active(
        self, sync_id: UUID, sync_active_input: SyncsActiveUpdateInput
    ):
        pass
    
    @abstractmethod
    def delete_sync_active(self, sync_active_id: int, user_id: str):
        pass
    
    @abstractmethod
    def get_files_folder_active_sync(self, sync_active_id: int, folder_id: int = None):
        pass
    
    @abstractmethod
    def get_details_sync_active(self, sync_active_id: int):
        pass