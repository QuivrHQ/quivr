from quivr_api.logger import get_logger
from quivr_api.modules.dependencies import get_supabase_client
from quivr_api.modules.sync.dto.inputs import (
    SyncFileInput,
    SyncFileUpdateInput,
)
from quivr_api.modules.sync.entity.sync_models import DBSyncFile, SyncFile, SyncsActive
from quivr_api.modules.sync.repository.sync_interfaces import SyncFileInterface

logger = get_logger(__name__)


class SyncFilesRepository(SyncFileInterface):
    def __init__(self):
        """
        Initialize the SyncFiles class with a Supabase client.
        """
        supabase_client = get_supabase_client()
        self.db = supabase_client  # type: ignore
        logger.debug("Supabase client initialized")

    def create_sync_file(self, sync_file_input: SyncFileInput) -> DBSyncFile | None:
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
            return DBSyncFile(**response.data[0])
        logger.warning("Failed to create sync file")

    def get_sync_files(self, sync_active_id: int) -> list[DBSyncFile]:
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
            return [DBSyncFile(**file) for file in response.data]
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
        self.db.from_("syncs_files").update(
            sync_file_input.model_dump(exclude_unset=True)
        ).eq("id", sync_file_id).execute()
        logger.info("Sync file updated successfully")

    def update_or_create_sync_file(
        self,
        file: SyncFile,
        sync_active: SyncsActive,
        previous_file: DBSyncFile | None,
        supported: bool,
    ) -> DBSyncFile | None:
        if previous_file:
            logger.debug(f"Upserting file {previous_file} in database.")
            sync_file = self.update_sync_file(
                previous_file.id,
                SyncFileUpdateInput(
                    last_modified=file.last_modified,
                    supported=previous_file.supported or supported,
                ),
            )
        else:
            logger.debug("Creating new file in database.")
            sync_file = self.create_sync_file(
                SyncFileInput(
                    path=file.name,
                    syncs_active_id=sync_active.id,
                    last_modified=file.last_modified,
                    brain_id=str(sync_active.brain_id),
                    supported=supported,
                )
            )
        return sync_file

    def delete_sync_file(self, sync_file_id: int):
        """
        Delete a sync file from the database.

        Args:
            sync_file_id (int): The ID of the sync file.
        """
        logger.info("Deleting sync file with sync_file_id: %s", sync_file_id)
        self.db.from_("syncs_files").delete().eq("id", sync_file_id).execute()
        logger.info("Sync file deleted successfully")
