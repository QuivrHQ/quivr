from sqlite3 import IntegrityError
from typing import Any, List
from uuid import UUID

from sqlmodel import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_api.logger import get_logger
from quivr_api.modules.dependencies import BaseRepository, get_supabase_client
from quivr_api.modules.sync.dto.inputs import SyncCreateInput, SyncUpdateInput
from quivr_api.modules.sync.dto.outputs import SyncProvider
from quivr_api.modules.sync.entity.sync_models import Sync, SyncFile
from quivr_api.modules.sync.repository.notion_repository import NotionRepository
from quivr_api.modules.sync.service.sync_notion import SyncNotionService
from quivr_api.modules.sync.utils.sync import (
    AzureDriveSync,
    BaseSync,
    DropboxSync,
    GitHubSync,
    GoogleDriveSync,
    NotionSync,
)
from quivr_api.modules.sync.utils.sync_exceptions import (
    SyncEmptyCredentials,
    SyncNotFoundException,
    SyncProviderError,
    SyncUpdateError,
)

logger = get_logger(__name__)


class SyncsRepository(BaseRepository):
    def __init__(
        self,
        session: AsyncSession,
        sync_provider_mapping: dict[SyncProvider, BaseSync] | None = None,
    ):
        self.session = session
        self.db = get_supabase_client()

        if sync_provider_mapping is None:
            self.sync_provider_mapping: dict[SyncProvider, BaseSync] = {
                SyncProvider.GOOGLE: GoogleDriveSync(),
                SyncProvider.DROPBOX: DropboxSync(),
                SyncProvider.AZURE: AzureDriveSync(),
                SyncProvider.NOTION: NotionSync(
                    notion_service=SyncNotionService(NotionRepository(self.session))
                ),
                SyncProvider.GITHUB: GitHubSync(),
            }
        else:
            self.sync_provider_mapping = sync_provider_mapping

    async def create_sync(
        self,
        sync_user_input: SyncCreateInput,
    ) -> Sync:
        """
        Create a new sync user in the database.

        Args:
            sync_user_input (SyncsUserInput): The input data for creating a sync user.

        Returns:
        """
        logger.info("Creating sync user with input: %s", sync_user_input)
        try:
            sync = Sync.model_validate(sync_user_input.model_dump())
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

    async def get_sync_id(self, sync_id: int, user_id: UUID | None = None) -> Sync:
        """
        Retrieve sync users from the database.
        """
        query = select(Sync).where(Sync.id == sync_id)

        if user_id:
            query = query.where(Sync.user_id == user_id)
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
        query = select(Sync).where(Sync.user_id == user_id)
        if sync_id is not None:
            query = query.where(Sync.id == sync_id)
        result = await self.session.exec(query)
        return list(result.all())

    async def get_sync_user_by_state(self, state: dict) -> Sync:
        """
        Retrieve a sync user by their state.

        Args:
            state (dict): The state to filter sync users.

        Returns:
            dict or None: The sync user data matching the state or None if not found.
        """
        logger.info("Getting sync user by state: %s", state)

        query = select(Sync).where(Sync.state == state)
        result = await self.session.exec(query)
        sync = result.first()
        if not sync:
            raise SyncNotFoundException()
        return sync

        return None

    async def delete_sync(self, sync_id: int, user_id: UUID):
        logger.info(
            "Deleting sync user with sync_id: %s, user_id: %s", sync_id, user_id
        )
        await self.session.execute(
            delete(Sync).where(Sync.id == sync_id).where(Sync.user_id == user_id)  # type: ignore
        )
        logger.info("Sync user deleted successfully")

    async def update_sync(
        self, sync: Sync, sync_input: SyncUpdateInput | dict[str, Any]
    ):
        logger.debug(
            f"Updating sync {sync.id} with input: {sync_input}",
        )
        try:
            if isinstance(sync_input, dict):
                update_data = sync_input
            else:
                update_data = sync_input.model_dump(exclude_unset=True)
            for field in update_data:
                setattr(sync, field, update_data[field])

            self.session.add(sync)
            await self.session.commit()
            await self.session.refresh(sync)
            return sync
        except IntegrityError as e:
            await self.session.rollback()
            logger.error(f"Error updating knowledge {e}")
            raise SyncUpdateError

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
        sync_id: int,
        user_id: UUID,
        folder_id: str | None = None,
        recursive: bool = False,
    ) -> List[SyncFile] | None:
        logger.info(
            "Retrieving files for user sync with sync_active_id: %s, user_id: %s, folder_id: %s",
            sync_id,
            user_id,
            folder_id,
        )
        sync = await self.get_sync_id(sync_id=sync_id, user_id=user_id)
        if not sync:
            logger.error(
                "No sync user found for sync_active_id: %s, user_id: %s",
                sync_id,
                user_id,
            )
            return None

        try:
            sync_provider = self.sync_provider_mapping[
                SyncProvider(sync.provider.lower())
            ]
        except KeyError:
            raise SyncProviderError

        if sync.credentials is None:
            raise SyncEmptyCredentials

        return await sync_provider.aget_files(
            sync.credentials, folder_id if folder_id else "", recursive
        )
