from abc import ABC, abstractmethod
from typing import Dict, List, Union
from uuid import UUID

from quivr_api.logger import get_logger
from quivr_api.modules.sync.dto.inputs import (
    SyncsActiveInput,
    SyncsActiveUpdateInput,
    SyncsUserInput,
    SyncsUserStatus,
    SyncUserUpdateInput,
)
from quivr_api.modules.sync.entity.sync_models import SyncsActive, SyncsUser
from quivr_api.modules.sync.repository.sync_repository import Sync
from quivr_api.modules.sync.repository.sync_user import SyncUserRepository
from quivr_api.modules.sync.service.sync_notion import SyncNotionService

logger = get_logger(__name__)


class ISyncUserService(ABC):
    @abstractmethod
    def get_syncs_user(self, user_id: UUID, sync_user_id: Union[int, None] = None):
        pass

    @abstractmethod
    def create_sync_user(self, sync_user_input: SyncsUserInput):
        pass

    @abstractmethod
    def delete_sync_user(self, sync_id: int, user_id: str):
        pass

    @abstractmethod
    def get_sync_user_by_state(self, state: Dict) -> Union["SyncsUser", None]:
        pass

    @abstractmethod
    def get_sync_user_by_id(self, sync_id: int):
        pass

    @abstractmethod
    def update_sync_user(
        self, sync_user_id: UUID, state: Dict, sync_user_input: SyncUserUpdateInput
    ):
        pass

    @abstractmethod
    def get_all_notion_user_syncs(self):
        pass

    @abstractmethod
    async def get_files_folder_user_sync(
        self,
        sync_active_id: int,
        user_id: UUID,
        folder_id: Union[str, None] = None,
        recursive: bool = False,
        notion_service: Union["SyncNotionService", None] = None,
    ):
        pass


class SyncUserService(ISyncUserService):
    def __init__(self):
        self.repository = SyncUserRepository()

    def get_syncs_user(self, user_id: UUID, sync_user_id: int | None = None):
        return self.repository.get_syncs_user(user_id, sync_user_id)

    def create_sync_user(self, sync_user_input: SyncsUserInput):
        if sync_user_input.provider == "Notion":
            response = self.repository.get_corresponding_deleted_sync(
                user_id=sync_user_input.user_id
            )
            if response:
                raise ValueError("User removed this connection less than 24 hours ago")

        return self.repository.create_sync_user(sync_user_input)

    def delete_sync_user(self, sync_id: int, user_id: str):
        sync_user = self.repository.get_sync_user_by_id(sync_id)
        if sync_user and sync_user.provider == "Notion":
            sync_user_input = SyncUserUpdateInput(
                email=str(sync_user.email),
                credentials=sync_user.credentials,
                state=sync_user.state,
                status=str(SyncsUserStatus.REMOVED),
            )
            self.repository.update_sync_user(
                sync_user_id=sync_user.user_id,
                state=sync_user.state,
                sync_user_input=sync_user_input,
            )
            return None
        else:
            return self.repository.delete_sync_user(sync_id, user_id)

    def clean_notion_user_syncs(self):
        return self.repository.clean_notion_user_syncs()

    def get_sync_user_by_state(self, state: dict) -> SyncsUser | None:
        return self.repository.get_sync_user_by_state(state)

    def get_sync_user_by_id(self, sync_id: int):
        return self.repository.get_sync_user_by_id(sync_id)

    def update_sync_user(
        self, sync_user_id: UUID, state: dict, sync_user_input: SyncUserUpdateInput
    ):
        return self.repository.update_sync_user(sync_user_id, state, sync_user_input)

    def update_sync_user_status(self, sync_user_id: int, status: str):
        return self.repository.update_sync_user_status(sync_user_id, status)

    def get_all_notion_user_syncs(self):
        return self.repository.get_all_notion_user_syncs()

    async def get_files_folder_user_sync(
        self,
        sync_active_id: int,
        user_id: UUID,
        folder_id: str | None = None,
        recursive: bool = False,
        notion_service: SyncNotionService | None = None,
    ):
        return await self.repository.get_files_folder_user_sync(
            sync_active_id=sync_active_id,
            user_id=user_id,
            folder_id=folder_id,
            recursive=recursive,
            notion_service=notion_service,
        )


class ISyncService(ABC):
    @abstractmethod
    def create_sync_active(
        self, sync_active_input: SyncsActiveInput, user_id: str
    ) -> Union["SyncsActive", None]:
        pass

    @abstractmethod
    def get_syncs_active(self, user_id: str) -> List[SyncsActive]:
        pass

    @abstractmethod
    def update_sync_active(
        self, sync_id: int, sync_active_input: SyncsActiveUpdateInput
    ):
        pass

    @abstractmethod
    def delete_sync_active(self, sync_active_id: int, user_id: UUID):
        pass

    @abstractmethod
    async def get_syncs_active_in_interval(self) -> List[SyncsActive]:
        pass

    @abstractmethod
    def get_details_sync_active(self, sync_active_id: int):
        pass


class SyncService(ISyncService):
    def __init__(self):
        self.repository = Sync()

    def create_sync_active(
        self, sync_active_input: SyncsActiveInput, user_id: str
    ) -> SyncsActive | None:
        return self.repository.create_sync_active(sync_active_input, user_id)

    def get_syncs_active(self, user_id: str) -> List[SyncsActive]:
        return self.repository.get_syncs_active(user_id)

    def update_sync_active(
        self, sync_id: int, sync_active_input: SyncsActiveUpdateInput
    ):
        return self.repository.update_sync_active(sync_id, sync_active_input)

    def delete_sync_active(self, sync_active_id: int, user_id: UUID):
        return self.repository.delete_sync_active(sync_active_id, user_id)

    async def get_syncs_active_in_interval(self) -> List[SyncsActive]:
        return await self.repository.get_syncs_active_in_interval()

    def get_details_sync_active(self, sync_active_id: int):
        return self.repository.get_details_sync_active(sync_active_id)
