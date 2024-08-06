from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from quivr_api.modules.sync.dto.inputs import (
    SyncFileInput,
    SyncFileUpdateInput,
    SyncsActiveInput,
    SyncsActiveUpdateInput,
    SyncsUserInput,
    SyncUserUpdateInput,
)
from quivr_api.modules.sync.entity.sync import SyncsActive, SyncsFiles


class SyncUserInterface(ABC):
    @abstractmethod
    def create_sync_user(
        self,
        sync_user_input: SyncsUserInput,
    ):
        pass

    @abstractmethod
    def get_syncs_user(self, user_id: str, sync_user_id: int = None):
        pass

    @abstractmethod
    def get_sync_user_by_id(self, sync_id: int):
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
    def get_files_folder_user_sync(
        self,
        sync_active_id: int,
        user_id: str,
        folder_id: int | str | None = None,
        recursive: bool = False,
    ):
        pass


class SyncInterface(ABC):
    @abstractmethod
    def create_sync_active(
        self,
        sync_active_input: SyncsActiveInput,
        user_id: str,
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
    def get_details_sync_active(self, sync_active_id: int):
        pass

    @abstractmethod
    async def get_syncs_active_in_interval(self) -> List[SyncsActive]:
        pass


class SyncFileInterface(ABC):
    @abstractmethod
    def create_sync_file(self, sync_file_input: SyncFileInput) -> SyncsFiles:
        pass

    @abstractmethod
    def get_sync_files(self, sync_active_id: int) -> list[SyncsFiles]:
        pass

    @abstractmethod
    def update_sync_file(self, sync_file_id: int, sync_file_input: SyncFileUpdateInput):
        pass

    @abstractmethod
    def delete_sync_file(self, sync_file_id: int):
        pass
