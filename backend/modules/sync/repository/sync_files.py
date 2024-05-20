from logger import get_logger
from models.settings import get_supabase_client
from modules.sync.dto.inputs import SyncFileInput, SyncFileUpdateInput
from modules.sync.entity.sync import SyncsFiles
from modules.sync.repository.sync_interfaces import SyncFileInterface

logger = get_logger(__name__)


class SyncFiles(SyncFileInterface):
    def __init__(self):
        """
        Initialize the SyncFiles class with a Supabase client.
        """
        supabase_client = get_supabase_client()
        self.db = supabase_client  # type: ignore
        logger.debug("Supabase client initialized")

    def create_sync_file(self, sync_file_input: SyncFileInput) -> SyncsFiles:
        """
        Create a new sync file in the database.

        Args:
            sync_file_input (SyncFileInput): The input data for creating a sync file.

        Returns:
            SyncsFiles: The created sync file data.
        """
        logger.info("Creating sync file with input: %s", sync_file_input)
        response = (
            self.db.from_("syncs_files")
            .insert(
                {
                    "path": sync_file_input.path,
                    "syncs_active_id": sync_file_input.syncs_active_id,
                    "last_modified": sync_file_input.last_modified,
                    "brain_id": sync_file_input.brain_id,
                }
            )
            .execute()
        )
        if response.data:
            logger.info("Sync file created successfully: %s", response.data[0])
            return SyncsFiles(**response.data[0])
        logger.warning("Failed to create sync file")
        return None

    def get_sync_files(self, sync_active_id: int) -> list[SyncsFiles]:
        """
        Retrieve sync files from the database.

        Args:
            sync_active_id (int): The ID of the active sync.

        Returns:
            list[SyncsFiles]: A list of sync files matching the criteria.
        """
        logger.info("Retrieving sync files for sync_active_id: %s", sync_active_id)
        response = (
            self.db.from_("syncs_files")
            .select("*")
            .eq("syncs_active_id", sync_active_id)
            .execute()
        )
        if response.data:
            # logger.info("Sync files retrieved successfully: %s", response.data)
            return [SyncsFiles(**file) for file in response.data]
        logger.warning("No sync files found for sync_active_id: %s", sync_active_id)
        return []

    def update_sync_file(self, sync_file_id: int, sync_file_input: SyncFileUpdateInput):
        """
        Update a sync file in the database.

        Args:
            sync_file_id (int): The ID of the sync file.
            sync_file_input (SyncFileUpdateInput): The input data for updating the sync file.
        """
        logger.info(
            "Updating sync file with sync_file_id: %s, input: %s",
            sync_file_id,
            sync_file_input,
        )
        self.db.from_("syncs_files").update(sync_file_input.model_dump()).eq(
            "id", sync_file_id
        ).execute()
        logger.info("Sync file updated successfully")

    def delete_sync_file(self, sync_file_id: int):
        """
        Delete a sync file from the database.

        Args:
            sync_file_id (int): The ID of the sync file.
        """
        logger.info("Deleting sync file with sync_file_id: %s", sync_file_id)
        self.db.from_("syncs_files").delete().eq("id", sync_file_id).execute()
        logger.info("Sync file deleted successfully")
