from datetime import datetime, timedelta
from typing import List, Sequence
from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_api.logger import get_logger
from quivr_api.modules.dependencies import BaseRepository, get_supabase_client
from quivr_api.modules.notification.service.notification_service import (
    NotificationService,
)
from quivr_api.modules.sync.dto.inputs import SyncsActiveInput, SyncsActiveUpdateInput
from quivr_api.modules.sync.entity.sync_models import NotionSyncFile, SyncsActive
from quivr_api.modules.sync.repository.sync_interfaces import SyncInterface

notification_service = NotificationService()

logger = get_logger(__name__)


class Sync(SyncInterface):
    def __init__(self):
        """
        Initialize the Sync class with a Supabase client.
        """
        supabase_client = get_supabase_client()
        self.db = supabase_client  # type: ignore
        logger.debug("Supabase client initialized")

    def create_sync_active(
        self, sync_active_input: SyncsActiveInput, user_id: str
    ) -> SyncsActive | None:
        """
        Create a new active sync in the database.

        Args:
            sync_active_input (SyncsActiveInput): The input data for creating an active sync.
            user_id (str): The user ID associated with the active sync.

        Returns:
            SyncsActive or None: The created active sync data or None if creation failed.
        """
        logger.info(
            "Creating active sync for user_id: %s with input: %s",
            user_id,
            sync_active_input,
        )
        sync_active_input_dict = sync_active_input.model_dump()
        sync_active_input_dict["user_id"] = user_id
        response = (
            self.db.from_("syncs_active").insert(sync_active_input_dict).execute()
        )
        if response.data:
            logger.info("Active sync created successfully: %s", response.data[0])
            return SyncsActive(**response.data[0])

        logger.error("Failed to create active sync for user_id: %s", user_id)

    def get_syncs_active(self, user_id: UUID | str) -> List[SyncsActive]:
        """
        Retrieve active syncs from the database.

        Args:
            user_id (str): The user ID to filter active syncs.

        Returns:
            List[SyncsActive]: A list of active syncs matching the criteria.
        """
        logger.info("Retrieving active syncs for user_id: %s", user_id)
        response = (
            self.db.from_("syncs_active")
            .select("*, syncs_user(*)")
            .eq("user_id", user_id)
            .execute()
        )
        if response.data:
            logger.info("Active syncs retrieved successfully: %s", response.data)
            return [SyncsActive(**sync) for sync in response.data]
        logger.warning("No active syncs found for user_id: %s", user_id)
        return []

    def update_sync_active(
        self, sync_id: int | str, sync_active_input: SyncsActiveUpdateInput
    ) -> SyncsActive | None:
        """
        Update an active sync in the database.

        Args:
            sync_id (int): The ID of the active sync.
            sync_active_input (SyncsActiveUpdateInput): The input data for updating the active sync.

        Returns:
            dict or None: The updated active sync data or None if update failed.
        """
        logger.info(
            "Updating active sync with sync_id: %s, input: %s",
            sync_id,
            sync_active_input,
        )

        response = (
            self.db.from_("syncs_active")
            .update(sync_active_input.model_dump(exclude_unset=True))
            .eq("id", sync_id)
            .execute()
        )

        if response.data:
            logger.info("Active sync updated successfully: %s", response.data[0])
            return SyncsActive.model_validate(response.data[0])

        logger.error("Failed to update active sync with sync_id: %s", sync_id)

    def delete_sync_active(self, sync_active_id: int, user_id: UUID):
        """
        Delete an active sync from the database.

        Args:
            sync_active_id (int): The ID of the active sync.
            user_id (str): The user ID associated with the active sync.

        Returns:
            dict or None: The deleted active sync data or None if deletion failed.
        """
        logger.info(
            "Deleting active sync with sync_active_id: %s, user_id: %s",
            sync_active_id,
            user_id,
        )
        response = (
            self.db.from_("syncs_active")
            .delete()
            .eq("id", sync_active_id)
            .eq("user_id", str(user_id))
            .execute()
        )
        if response.data:
            logger.info("Active sync deleted successfully: %s", response.data[0])
            return response.data[0]
        logger.warning(
            "Failed to delete active sync with sync_active_id: %s, user_id: %s",
            sync_active_id,
            user_id,
        )
        return None

    def get_details_sync_active(self, sync_active_id: int):
        """
        Retrieve details of an active sync, including associated sync user data.

        Args:
            sync_active_id (int): The ID of the active sync.

        Returns:
            dict or None: The detailed active sync data or None if not found.
        """
        logger.info(
            "Retrieving details for active sync with sync_active_id: %s", sync_active_id
        )
        response = (
            self.db.table("syncs_active")
            .select("*, syncs_user(provider, credentials)")
            .eq("id", sync_active_id)
            .execute()
        )
        if response.data:
            logger.info(
                "Details for active sync retrieved successfully: %s", response.data[0]
            )
            return response.data[0]
        logger.warning(
            "No details found for active sync with sync_active_id: %s", sync_active_id
        )
        return None

    async def get_syncs_active_in_interval(self) -> List[SyncsActive]:
        """
        Retrieve active syncs that are due for synchronization based on their interval.

        Returns:
            list: A list of active syncs that are due for synchronization.
        """
        logger.info("Retrieving active syncs due for synchronization")

        current_time = datetime.now()

        # The Query filters the active syncs based on the sync_interval_minutes field and last_synced timestamp
        response = (
            self.db.table("syncs_active")
            .select("*")
            .lt("last_synced", (current_time - timedelta(minutes=360)).isoformat())
            .execute()
        )

        force_sync = (
            self.db.table("syncs_active").select("*").eq("force_sync", True).execute()
        )
        merge_data = response.data + force_sync.data
        if merge_data:
            logger.info("Active syncs retrieved successfully: %s", merge_data)
            return [SyncsActive(**sync) for sync in merge_data]
        logger.info("No active syncs found due for synchronization")
        return []


class NotionRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.session = session
        self.db = get_supabase_client()

    async def get_user_notion_files(
        self, user_id: UUID, sync_user_id: int
    ) -> Sequence[NotionSyncFile]:
        query = select(NotionSyncFile).where(
            NotionSyncFile.user_id == user_id
            and NotionSyncFile.sync_user_id == sync_user_id
        )
        response = await self.session.exec(query)
        return response.all()

    async def create_notion_files(
        self, notion_files: List[NotionSyncFile]
    ) -> List[NotionSyncFile]:
        try:
            self.session.add_all(notion_files)
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise Exception("Integrity error while creating notion files.")
        except Exception as e:
            await self.session.rollback()
            raise e

        return notion_files

    async def update_notion_file(self, updated_notion_file: NotionSyncFile) -> bool:
        try:
            is_update = False
            query = select(NotionSyncFile).where(
                NotionSyncFile.notion_id == updated_notion_file.notion_id
            )
            result = await self.session.exec(query)
            existing_page = result.one_or_none()

            if existing_page:
                # Update existing page
                existing_page.name = updated_notion_file.name
                existing_page.last_modified = updated_notion_file.last_modified
                self.session.add(existing_page)
                is_update = True
            else:
                # Add new page
                self.session.add(updated_notion_file)

            await self.session.commit()

            # Refresh the object that's actually in the session
            refreshed_file = existing_page if existing_page else updated_notion_file
            await self.session.refresh(refreshed_file)

            logger.info(f"Updated notion file in notion repo: {refreshed_file}")
            return is_update

        except IntegrityError as ie:
            logger.error(f"IntegrityError occurred: {ie}")
            await self.session.rollback()
            raise Exception("Integrity error while updating notion file.")
        except Exception as e:
            logger.error(f"Exception occurred: {e}")
            await self.session.rollback()
            raise

    async def get_notion_files_by_ids(self, ids: List[str]) -> Sequence[NotionSyncFile]:
        query = select(NotionSyncFile).where(NotionSyncFile.notion_id.in_(ids))  # type: ignore
        response = await self.session.exec(query)
        return response.all()

    async def get_notion_files_by_parent_id(
        self, parent_id: str | None, sync_user_id: int
    ) -> Sequence[NotionSyncFile]:
        query = (
            select(NotionSyncFile)
            .where(NotionSyncFile.parent_id == parent_id)
            .where(NotionSyncFile.sync_user_id == sync_user_id)
        )
        response = await self.session.exec(query)
        return response.all()

    async def get_all_notion_files(self) -> Sequence[NotionSyncFile]:
        query = select(NotionSyncFile)
        response = await self.session.exec(query)
        return response.all()

    async def is_folder_page(self, page_id: str) -> bool:
        query = select(NotionSyncFile).where(NotionSyncFile.parent_id == page_id)
        response = await self.session.exec(query)
        return response.first() is not None

    async def delete_notion_page(self, notion_id: UUID):
        query = select(NotionSyncFile).where(NotionSyncFile.notion_id == notion_id)
        response = await self.session.exec(query)
        notion_file = response.first()
        if notion_file:
            await self.session.delete(notion_file)
            await self.session.commit()
            return notion_file
        return None

    async def delete_notion_pages(self, notion_ids: List[UUID]):
        query = select(NotionSyncFile).where(
            or_(
                col(NotionSyncFile.notion_id).in_(notion_ids),
                col(NotionSyncFile.parent_id).in_(notion_ids),
            )
        )
        response = await self.session.exec(query)
        notion_files = response.all()
        if notion_files:
            for notion_file in notion_files:
                await self.session.delete(notion_file)
            await self.session.commit()
            return notion_files
        return None
