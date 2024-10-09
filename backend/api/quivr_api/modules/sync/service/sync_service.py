from typing import Any
from uuid import UUID

from fastapi import HTTPException

from quivr_api.logger import get_logger
from quivr_api.modules.dependencies import BaseService
from quivr_api.modules.sync.dto.inputs import (
    SyncCreateInput,
    SyncStatus,
    SyncUpdateInput,
)
from quivr_api.modules.sync.dto.outputs import SyncsOutput
from quivr_api.modules.sync.repository.sync_repository import SyncsRepository
from quivr_api.modules.sync.utils.oauth2 import Oauth2BaseState, Oauth2State

logger = get_logger(__name__)


class SyncsService(BaseService[SyncsRepository]):
    repository_cls = SyncsRepository

    def __init__(self, repository: SyncsRepository):
        self.repository = repository

    async def create_sync_user(self, sync_user_input: SyncCreateInput) -> SyncsOutput:
        sync = await self.repository.create_sync(sync_user_input)
        return sync.to_dto()

    async def get_user_syncs(self, user_id: UUID, sync_id: int | None = None):
        return await self.repository.get_syncs(user_id=user_id, sync_id=sync_id)

    async def delete_sync(self, sync_id: int, user_id: UUID):
        await self.repository.delete_sync(sync_id, user_id)

    async def get_sync_by_id(self, sync_id: int):
        return await self.repository.get_sync_id(sync_id)

    async def get_from_oauth2_state(self, state: Oauth2State) -> SyncsOutput:
        assert state.sync_id, "state should have associated sync_id"
        sync = await self.get_sync_by_id(state.sync_id)

        # TODO: redo these exceptions
        if (
            not sync
            or not sync.state
            or state.model_dump_json(exclude={"sync_id"}) != sync.state["state"]
        ):
            logger.error("Invalid state parameter")
            raise HTTPException(status_code=400, detail="Invalid state parameter")
        if sync.user_id != state.user_id:
            raise HTTPException(status_code=400, detail="Invalid user")
        return sync.to_dto()

    async def create_oauth2_state(
        self,
        provider: str,
        name: str,
        user_id: UUID,
        additional_data: dict[str, Any] = {},
    ) -> Oauth2State:
        state_struct = Oauth2BaseState(name=name, user_id=user_id)
        state = state_struct.model_dump_json()
        sync_user_input = SyncCreateInput(
            name=name,
            user_id=user_id,
            provider=provider,
            credentials={},
            state={"state": state},
            additional_data=additional_data,
            status=SyncStatus.SYNCING,
        )
        sync = await self.create_sync_user(sync_user_input)
        return Oauth2State(sync_id=sync.id, **state_struct.model_dump())

    async def update_sync(
        self, sync_id: int, sync_user_input: SyncUpdateInput
    ) -> SyncsOutput:
        sync = await self.repository.get_sync_id(sync_id)
        sync = await self.repository.update_sync(sync, sync_user_input)
        return sync.to_dto()

    async def get_all_notion_user_syncs(self):
        return self.repository.get_all_notion_user_syncs()

    async def get_files_folder_user_sync(
        self,
        sync_active_id: int,
        user_id: UUID,
        folder_id: str | None = None,
        recursive: bool = False,
    ):
        return await self.repository.get_files_folder_user_sync(
            sync_id=sync_active_id,
            user_id=user_id,
            folder_id=folder_id,
            recursive=recursive,
        )
