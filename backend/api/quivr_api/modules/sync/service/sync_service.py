from uuid import UUID

from quivr_api.logger import get_logger
from quivr_api.modules.dependencies import BaseService
from quivr_api.modules.sync.dto.inputs import (
    SyncCreateInput,
    SyncUpdateInput,
)
from quivr_api.modules.sync.dto.outputs import SyncsOutput
from quivr_api.modules.sync.repository.sync_repository import SyncsRepository
from quivr_api.modules.sync.service.sync_notion import SyncNotionService

logger = get_logger(__name__)


class SyncsService(BaseService[SyncsRepository]):
    repository_cls = SyncsRepository

    def __init__(self, repository: SyncsRepository):
        self.repository = repository

    async def create_sync_user(self, sync_user_input: SyncCreateInput) -> SyncsOutput:
        sync = await self.repository.create_sync(sync_user_input)
        return sync.to_dto()

    def get_syncs(self, user_id: UUID, sync_id: int | None = None):
        return self.repository.get_syncs(user_id, sync_id)

    def delete_sync(self, sync_id: int, user_id: str):
        return self.repository.delete_sync(sync_id, user_id)

    def get_sync_by_state(self, state: dict) -> SyncsOutput | None:
        return self.repository.get_sync_user_by_state(state)

    def get_sync_by_id(self, sync_id: int):
        return self.repository.get_sync_id(sync_id)

    def update_sync(
        self, sync_user_id: UUID, state: dict, sync_user_input: SyncUpdateInput
    ):
        return self.repository.update_sync(sync_user_id, state, sync_user_input)

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
