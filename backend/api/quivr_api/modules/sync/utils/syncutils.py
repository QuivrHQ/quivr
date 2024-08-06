import io
from datetime import datetime, timedelta, timezone
from typing import List, Tuple
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict
from supabase.client import AsyncClient

from quivr_api.logger import get_logger
from quivr_api.models.settings import get_supabase_async_client
from quivr_api.modules.brain.repository.brains_vectors import BrainsVectors
from quivr_api.modules.knowledge.repository.storage import Storage
from quivr_api.modules.notification.dto.inputs import (
    CreateNotification,
    NotificationUpdatableProperties,
)
from quivr_api.modules.notification.entity.notification import NotificationsStatusEnum
from quivr_api.modules.notification.service.notification_service import (
    NotificationService,
)
from quivr_api.modules.sync.dto.inputs import (
    SyncFileInput,
    SyncFileUpdateInput,
    SyncsActiveUpdateInput,
)
from quivr_api.modules.sync.entity.sync import DBSyncFile, SyncFile
from quivr_api.modules.sync.repository.sync_files import SyncFiles
from quivr_api.modules.sync.service.sync_service import SyncService, SyncUserService
from quivr_api.modules.sync.utils.sync import BaseSync
from quivr_api.modules.upload.service.upload_file import (
    check_file_exists,
    upload_file_storage,
)

notification_service = NotificationService()
brain_vectors = BrainsVectors()
logger = get_logger(__name__)


def filter_supported_files(
    files: list[SyncFile], existing_files: dict[str, DBSyncFile]
) -> list[Tuple[SyncFile, DBSyncFile | None]]:
    res = []
    for new_file in files:
        prev_file = existing_files.get(new_file.name, None)
        if (prev_file and prev_file.supported) or prev_file is None:
            res.append((new_file, prev_file))

    return res


def create_sync_bulk_notification(
    files: list[SyncFile], current_user: UUID, brain_id: UUID, bulk_id: UUID
):
    # TODO(@chloedia): redo this, we don't UploadFile as an additional abstraction
    for file in files:
        upload_notification = notification_service.add_notification(
            CreateNotification(
                user_id=current_user,
                bulk_id=bulk_id,
                status=NotificationsStatusEnum.INFO,
                title=file.name,
                category="sync",
                brain_id=str(brain_id),
            )
        )
        file.notification_id = str(upload_notification.id)


class SyncUtils(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    sync_user_service: SyncUserService
    sync_active_service: SyncService
    sync_files_repo: SyncFiles
    storage: Storage
    sync_cloud: BaseSync

    def _upsert_sync_file(
        self,
        file_name: str,
        brain_id: UUID,
        modified_time: str,
        previous_file: DBSyncFile | None,
        sync_active_id: int,
    ):
        if previous_file:
            logger.debug(f"Updating file {previous_file} in database.")
            self.sync_files_repo.update_sync_file(
                previous_file.id,
                SyncFileUpdateInput(
                    last_modified=modified_time,
                    supported=previous_file.supported,
                ),
            )
        else:
            # Create a new file record
            self.sync_files_repo.create_sync_file(
                SyncFileInput(
                    path=file_name,
                    syncs_active_id=sync_active_id,
                    last_modified=modified_time,
                    brain_id=str(brain_id),
                    supported=True,
                )
            )

    async def _process_sync_file(
        self,
        client: AsyncClient,
        file: SyncFile,
        previous_file: DBSyncFile | None,
        credentials: dict,
        current_user: UUID,
        brain_id: UUID,
        sync_active_id: int,
    ):
        logger.info("Processing file: %s", file.name)
        file_name, modified_time = file.name, file.last_modified

        if file_name.split(".")[-1] not in [
            "pdf",
            "txt",
            "md",
            "csv",
            "docx",
            "xlsx",
            "pptx",
            "doc",
        ]:
            logger.info("File is not compatible: %s. Skipping processing", file_name)
            return None

        # FIXME(@aminediro, @chloedia): Checks should use file_sha1 in database
        if check_file_exists(str(brain_id), str(file_name)):
            brain_vectors.delete_file_from_brain(brain_id, file_name)

        # TODO: function
        # TODO: Encode response in some Type for type checking
        logger.debug(f"Downloading {file} using {self.sync_cloud}")
        file_response = self.sync_cloud.download_file(credentials, file)
        logger.debug(f"Fetch sync file : {file_response}")
        file_name = str(file_response["file_name"])
        raw_data = file_response["content"]
        file_data = (
            io.BufferedReader(raw_data)  # type: ignore
            if isinstance(raw_data, io.BytesIO)
            else io.BufferedReader(raw_data.encode("utf-8"))  # type: ignore
        )

        # TODO:
        # check_user_limits()
        # Upload File to S3 Storage
        storage_path = str(brain_id) + "/" + str(file_name)
        await upload_file_storage(client, file_data, storage_path, upsert=True)

        # TODO
        # Add knowledge and send_task
        # Send file for processing

        self._upsert_sync_file(
            file_name=file_name,
            brain_id=brain_id,
            modified_time=modified_time,
            previous_file=previous_file,
            sync_active_id=sync_active_id,
        )

        notification_service.update_notification_by_id(
            file.notification_id,
            NotificationUpdatableProperties(
                status=NotificationsStatusEnum.SUCCESS,
                description="File downloaded successfully",
            ),
        )

    async def _process_sync_diff(
        self,
        credentials: dict,
        files: List[SyncFile],
        current_user: UUID,
        brain_id: UUID,
        sync_active_id: int,
    ):
        """
        Download files from an external cloud.

        Args:
            credentials (dict): The token data for accessing the external cloud.
            files (list): The list of file metadata to download.

        Returns:
            dict: A dictionary containing the status of the download or an error message.
        """

        client = await get_supabase_async_client()
        credentials = self.sync_cloud.check_and_refresh_access_token(credentials)

        downloaded_files = []
        bulk_id = uuid4()

        list_existing_files = self.sync_files_repo.get_sync_files(sync_active_id)
        existing_files = {f.path: f for f in list_existing_files}

        supported_files = filter_supported_files(files, existing_files)

        # TODO: bulk insert in batch
        create_sync_bulk_notification(files, current_user, brain_id, bulk_id)

        for file, prev_file in supported_files:
            try:
                result = await self._process_sync_file(
                    file=file,
                    previous_file=prev_file,
                    brain_id=brain_id,
                    client=client,
                    credentials=credentials,
                    current_user=current_user,
                    sync_active_id=sync_active_id,
                )
                if result is not None:
                    downloaded_files.append(result)

            except Exception as error:
                logger.error(
                    "An error occurred while downloading %s files: %s",
                    self.sync_cloud.name,
                    error,
                )
                # Check if the file already exists in the database
                existing_file = existing_files.get(file.name, None)

                # Update the existing file record
                if existing_file:
                    self.sync_files_repo.update_sync_file(
                        existing_file.id,
                        SyncFileUpdateInput(
                            supported=False,
                        ),
                    )
                else:
                    # Create a new file record
                    self.sync_files_repo.create_sync_file(
                        SyncFileInput(
                            path=file.name,
                            syncs_active_id=sync_active_id,
                            last_modified=file.last_modified,
                            # TODO(@chlo)
                            brain_id=str(brain_id),
                            supported=False,
                        )
                    )
                notification_service.update_notification_by_id(
                    file.notification_id,
                    NotificationUpdatableProperties(
                        status=NotificationsStatusEnum.ERROR,
                        description="Error downloading file",
                    ),
                )

        return {"downloaded_files": downloaded_files}

    async def sync(self, sync_active_id: int, user_id: UUID):
        """
        Check if the Specific sync has not been synced and download the folders and files based on the settings.

        Args:
            sync_active_id (int): The ID of the active sync.
            user_id (str): The user ID associated with the active sync.
        """

        # Retrieve the active sync details
        sync_active = self.sync_active_service.get_details_sync_active(sync_active_id)
        if not sync_active:
            logger.warning(
                "No active sync found for sync_active_id: %s", sync_active_id
            )
            return None

        # Check if the sync is due
        last_synced = sync_active.get("last_synced")
        force_sync = sync_active.get("force_sync", False)
        sync_interval_minutes = sync_active.get("sync_interval_minutes", 0)
        if last_synced and not force_sync:
            last_synced_time = datetime.fromisoformat(last_synced).astimezone(
                timezone.utc
            )
            current_time = datetime.now().astimezone()

            # Debug logging to check the values
            logger.debug("Last synced time (UTC): %s", last_synced_time)
            logger.debug("Current time (local timezone): %s", current_time)

            # Convert current_time to UTC for comparison
            current_time_utc = current_time.astimezone(timezone.utc)
            logger.debug("Current time (UTC): %s", current_time_utc)
            time_difference = current_time_utc - last_synced_time
            if time_difference < timedelta(minutes=sync_interval_minutes):
                logger.info(
                    "%s sync is not due for sync_active_id: %s",
                    self.sync_cloud.name,
                    sync_active_id,
                )
                return None

        # Retrieve the sync user details
        sync_user = self.sync_user_service.get_syncs_user(
            user_id=user_id, sync_user_id=sync_active["syncs_user_id"]
        )
        if not sync_user:
            logger.warning(
                "No sync user found for sync_active_id: %s, user_id: %s",
                sync_active_id,
                user_id,
            )
            return None

        sync_user = sync_user[0]
        if sync_user["provider"].lower() != self.sync_cloud.lower_name:
            logger.warning(
                "Sync provider is not %s for sync_active_id: %s",
                self.sync_cloud.name,
                sync_active_id,
            )
            return None

        # Download the folders and files from Cloud
        logger.info(
            "Downloading folders and files from %s for sync_active_id: %s",
            self.sync_cloud.name,
            sync_active_id,
        )

        # Get the folder id from the settings from sync_active
        settings = sync_active.get("settings", {})
        folders = settings.get("folders", [])
        files_to_download = settings.get("files", [])
        files: List[SyncFile] = []
        files_metadata = []
        if len(folders) > 0:
            for folder in folders:
                files.extend(
                    self.sync_cloud.get_files(
                        sync_user["credentials"],
                        folder_id=folder,
                        recursive=True,
                    )
                )
        if len(files_to_download) > 0:
            files_metadata = self.sync_cloud.get_files_by_id(
                sync_user["credentials"],
                files_to_download,
            )
        files = files + files_metadata  # type: ignore

        if "error" in files:
            logger.error(
                "Failed to download files from Azure for sync_active_id: %s",
                sync_active_id,
            )
            return None

        # Filter files that have been modified since the last sync
        last_synced_time = (
            datetime.fromisoformat(last_synced).astimezone(timezone.utc)
            if last_synced
            else None
        )
        logger.info("Files retrieved from %s: %s", self.sync_cloud.lower_name, files)

        files_to_download = [
            file
            for file in files
            if not file.is_folder
            and (
                (
                    not last_synced_time
                    or datetime.strptime(
                        file.last_modified,
                        (self.sync_cloud.datetime_format),
                    ).replace(tzinfo=timezone.utc)
                    > last_synced_time
                )
                or not check_file_exists(sync_active["brain_id"], file.name)
            )
        ]

        downloaded_files = await self._process_sync_diff(
            sync_user["credentials"],
            files_to_download,
            user_id,
            sync_active["brain_id"],
            sync_active_id,
        )
        if "error" in downloaded_files:
            logger.error(
                "Failed to download files from Azure for sync_active_id: %s",
                sync_active_id,
            )
            return None

        # Update the last_synced timestamp
        self.sync_active_service.update_sync_active(
            sync_active_id,
            SyncsActiveUpdateInput(
                last_synced=datetime.now().astimezone().isoformat(), force_sync=False
            ),
        )
        logger.info(
            "%s sync completed for sync_active_id: %s",
            self.sync_cloud.lower_name,
            sync_active_id,
        )
        return downloaded_files
