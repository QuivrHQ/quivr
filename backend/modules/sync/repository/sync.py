from datetime import datetime, timedelta
from typing import List

from logger import get_logger
from models.settings import get_supabase_client
from modules.knowledge.service.knowledge_service import KnowledgeService
from modules.notification.service.notification_service import NotificationService
from modules.sync.dto.inputs import SyncsActiveInput, SyncsActiveUpdateInput
from modules.sync.entity.sync import SyncsActive
from modules.sync.repository.sync_interfaces import SyncInterface

notification_service = NotificationService()
knowledge_service = KnowledgeService()
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
    ) -> SyncsActive:
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
        logger.warning("Failed to create active sync for user_id: %s", user_id)
        return None

    def get_syncs_active(self, user_id: str) -> List[SyncsActive]:
        """
        Retrieve active syncs from the database.

        Args:
            user_id (str): The user ID to filter active syncs.

        Returns:
            List[SyncsActive]: A list of active syncs matching the criteria.
        """
        logger.info("Retrieving active syncs for user_id: %s", user_id)
        response = (
            self.db.from_("syncs_active").select("*").eq("user_id", user_id).execute()
        )
        if response.data:
            logger.info("Active syncs retrieved successfully: %s", response.data)
            return [SyncsActive(**sync) for sync in response.data]
        logger.warning("No active syncs found for user_id: %s", user_id)
        return []

    def update_sync_active(
        self, sync_id: int, sync_active_input: SyncsActiveUpdateInput
    ):
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
            return response.data[0]
        logger.warning("Failed to update active sync with sync_id: %s", sync_id)
        return None

    def delete_sync_active(self, sync_active_id: int, user_id: str):
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
            .eq("user_id", user_id)
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
        if response.data:
            logger.info("Active syncs retrieved successfully: %s", response.data)
            for sync in response.data:
                # Now we can call the sync_google_drive_if_not_synced method to sync the Google Drive files
                logger.info("Syncing Google Drive for sync_active_id: %s", sync["id"])

            return [SyncsActive(**sync) for sync in response.data]
        logger.warning("No active syncs found due for synchronization")
        return []
