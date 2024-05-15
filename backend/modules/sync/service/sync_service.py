from typing import List
from logger import get_logger
from modules.sync.dto.inputs import SyncsUserInput
from modules.sync.repository.sync import Sync
from modules.sync.repository.sync_interfaces import SyncInterface
from modules.user.service.user_service import UserService
from modules.sync.dto.inputs import SyncsActiveInput, SyncsActiveUpdateInput
from modules.sync.entity.sync import SyncsActive

logger = get_logger(__name__)


user_service = UserService()


class SyncService:
    repository: SyncInterface

    def __init__(self):
        self.repository = Sync()

    def get_syncs_user(self, user_id: str):
        return self.repository.get_syncs_user(user_id)

    def create_sync_user(self, sync_user_input: SyncsUserInput):
        return self.repository.create_sync_user(sync_user_input)

    def delete_sync_user(self, sync_name: str, user_id: str):
        return self.repository.delete_sync_user(sync_name, user_id)

    def get_sync_user_by_state(self, state: dict):
        return self.repository.get_sync_user_by_state(state)

    def update_sync_user(self, sync_user_id: str, state: dict, sync_user_input: dict):
        return self.repository.update_sync_user(sync_user_id, state, sync_user_input)

    def create_sync_active(self, sync_active_input: SyncsActiveInput) -> SyncsActive:
        return self.repository.create_sync_active(sync_active_input)

    def get_syncs_active(self, user_id: str) -> List[SyncsActive]:
        return self.repository.get_syncs_active(user_id)

    def update_sync_active(self, sync_id: str, sync_active_input: SyncsActiveUpdateInput):
        return self.repository.update_sync_active(sync_id, sync_active_input)

    def delete_sync_active(self, sync_active_id: str, user_id: str):
        return self.repository.delete_sync_active(sync_active_id, user_id)

    def get_files_folder_active_sync(self, sync_active_id: str, folder_id: str = None):
        return self.repository.get_files_folder_active_sync(sync_active_id, folder_id)