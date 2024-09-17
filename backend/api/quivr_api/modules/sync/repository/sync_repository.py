import json
from sqlite3 import IntegrityError
from typing import List
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_api.logger import get_logger
from quivr_api.modules.dependencies import BaseRepository, get_supabase_client
from quivr_api.modules.sync.dto.inputs import SyncCreateInput, SyncUpdateInput
from quivr_api.modules.sync.dto.outputs import SyncProvider
from quivr_api.modules.sync.entity.sync_models import SyncFile, Syncs
from quivr_api.modules.sync.repository.notion_repository import NotionRepository
from quivr_api.modules.sync.service.sync_notion import SyncNotionService
from quivr_api.modules.sync.utils.exceptions import SyncNotFoundException
from quivr_api.modules.sync.utils.sync import (
    AzureDriveSync,
    BaseSync,
    DropboxSync,
    GitHubSync,
    GoogleDriveSync,
    NotionSync,
)
from quivr_api.modules.sync.utils.sync_exceptions import SyncEmptyCredentials

logger = get_logger(__name__)


class SyncsRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.db = get_supabase_client()

        self.sync_provider_mapping: dict[SyncProvider, BaseSync] = {
            SyncProvider.GOOGLE: GoogleDriveSync(),
            SyncProvider.DROPBOX: DropboxSync(),
            SyncProvider.AZURE: AzureDriveSync(),
            SyncProvider.NOTION: NotionSync(
                notion_service=SyncNotionService(NotionRepository(self.session))
            ),
            SyncProvider.GITHUB: GitHubSync(),
        }

    async def create_sync(
        self,
        sync_user_input: SyncCreateInput,
    ) -> Syncs:
        """
        Create a new sync user in the database.

        Args:
            sync_user_input (SyncsUserInput): The input data for creating a sync user.

        Returns:
        """
        logger.info("Creating sync user with input: %s", sync_user_input)
        try:
            sync = Syncs.model_validate(sync_user_input.model_dump())
            self.session.add(sync)
            await self.session.commit()
            await self.session.refresh(sync)
            return sync
        except IntegrityError:
            await self.session.rollback()
            raise
        except Exception:
            await self.session.rollback()
            raise

    async def get_sync_id(self, sync_id: int) -> Syncs | None:
        """
        Retrieve sync users from the database.
        """
        query = select(Syncs).where(Syncs.id == sync_id)
        result = await self.session.exec(query)
        sync = result.first()
        if not sync:
            logger.error(
                f"No sync user found for sync_id:  {sync_id}",
            )
            raise SyncNotFoundException()
        return sync

    async def get_syncs(self, user_id: UUID, sync_id: int | None = None):
        """
        Retrieve sync users from the database.

        Args:
            user_id (str): The user ID to filter sync users.
            sync_user_id (int, optional): The sync user ID to filter sync users. Defaults to None.

        Returns:
            list: A list of sync users matching the criteria.
        """
        logger.info(
            "Retrieving sync users for user_id: %s, sync_user_id: %s",
            user_id,
            sync_id,
        )
        query = select(Syncs).where(Syncs.id == sync_id).where(Syncs.user_id == user_id)
        result = await self.session.exec(query)
        sync = result.first()
        if not sync:
            logger.error(
                f"No sync user found for sync_id:  {sync_id}",
            )
            raise SyncNotFoundException()
        return sync

    async def get_sync_user_by_state(self, state: dict) -> Syncs | None:
        """
        Retrieve a sync user by their state.

        Args:
            state (dict): The state to filter sync users.

        Returns:
            dict or None: The sync user data matching the state or None if not found.
        """
        logger.info("Getting sync user by state: %s", state)

        query = select(Syncs).where(Syncs.state == state)
        result = await self.session.exec(query)
        sync = result.first()
        if not sync:
            raise SyncNotFoundException()
        return sync

        return None

    def delete_sync(self, sync_id: int, user_id: UUID | str):
        """
        Delete a sync user from the database.

        Args:
            provider (str): The provider of the sync user.
            user_id (str): The user ID of the sync user.
        """
        logger.info(
            "Deleting sync user with sync_id: %s, user_id: %s", sync_id, user_id
        )
        self.db.from_("syncs_user").delete().eq("id", sync_id).eq(
            "user_id", user_id
        ).execute()
        logger.info("Sync user deleted successfully")

    def update_sync_user(
        self, sync_user_id: UUID, state: dict, sync_user_input: SyncUpdateInput
    ):
        """
        Update a sync user in the database.

        Args:
            sync_user_id (str): The user ID of the sync user.
            state (dict): The state to filter sync users.
            sync_user_input (SyncUserUpdateInput): The input data for updating the sync user.
        """
        logger.info(
            "Updating sync user with user_id: %s, state: %s, input: %s",
            sync_user_id,
            state,
            sync_user_input,
        )

        state_str = json.dumps(state)
        self.db.from_("syncs_user").update(sync_user_input.model_dump()).eq(
            "user_id", str(sync_user_id)
        ).eq("state", state_str).execute()
        logger.info("Sync user updated successfully")

    def get_all_notion_user_syncs(self):
        """
        Retrieve all Notion sync users from the database.

        Returns:
            list: A list of Notion sync users.
        """
        logger.info("Retrieving all Notion sync users")
        response = (
            self.db.from_("syncs_user").select("*").eq("provider", "Notion").execute()
        )
        if response.data:
            logger.info("Notion sync users retrieved successfully")
            return response.data
        return []

    async def get_files_folder_user_sync(
        self,
        sync_active_id: int,
        user_id: UUID,
        folder_id: str | None = None,
        recursive: bool = False,
    ) -> List[SyncFile] | None:
        logger.info(
            "Retrieving files for user sync with sync_active_id: %s, user_id: %s, folder_id: %s",
            sync_active_id,
            user_id,
            folder_id,
        )
        sync_user = await self.get_syncs(user_id=user_id, sync_id=sync_active_id)
        if not sync_user:
            logger.error(
                "No sync user found for sync_active_id: %s, user_id: %s",
                sync_active_id,
                user_id,
            )
            return None

        provider = sync_user.provider.lower()
        sync_provider = self.sync_provider_mapping[SyncProvider(provider)]

        if sync_user.credentials is None:
            raise SyncEmptyCredentials

        return await sync_provider.aget_files(
            sync_user.credentials, folder_id if folder_id else "", recursive
        )
