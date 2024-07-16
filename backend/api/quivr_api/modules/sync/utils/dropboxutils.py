import os
import uuid
from datetime import datetime, timedelta, timezone
from io import BytesIO

import dropbox
from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict
from quivr_api.logger import get_logger
from quivr_api.modules.brain.repository.brains_vectors import BrainsVectors
from quivr_api.modules.knowledge.repository.storage import Storage
from quivr_api.modules.notification.dto.inputs import CreateNotification
from quivr_api.modules.notification.entity.notification import NotificationsStatusEnum
from quivr_api.modules.notification.service.notification_service import (
    NotificationService,
)
from quivr_api.modules.sync.dto.inputs import (
    SyncFileInput,
    SyncFileUpdateInput,
    SyncsActiveUpdateInput,
)
from quivr_api.modules.sync.repository.sync_files import SyncFiles
from quivr_api.modules.sync.service.sync_service import SyncService, SyncUserService
from quivr_api.modules.sync.utils.list_files import (
    get_dropbox_files_by_id,
    list_dropbox_files,
)
from quivr_api.modules.sync.utils.upload import upload_file
from quivr_api.modules.upload.service.upload_file import check_file_exists

logger = get_logger(__name__)

APP_KEY = os.getenv("DROPBOX_APP_KEY")
APP_SECRET = os.getenv("DROPBOW_CONSUMER_SECRET")

notification_service = NotificationService()


class DropboxSyncUtils(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    storage: Storage
    sync_files_repo: SyncFiles
    sync_active_service: SyncService
    sync_user_service: SyncUserService

    async def _upload_files(
        self,
        token_data: dict,
        files: list,
        current_user: str,
        brain_id: str,
        sync_active_id: int,
    ):
        """
        Download files from DropBox.

        Args:
            credentials (dict): The credentials for accessin DropBox Drive.
            files (list): The list of file metadata to download.

        Returns:
            dict: A dictionary containing the status of the download or an error message.
        """
        dbx = dropbox.Dropbox(token_data["access_token"])
        dbx.check_and_refresh_access_token()
        token_data["access_token"] = dbx._oauth2_access_token

        downloaded_files = []
        bulk_id = uuid.uuid4()

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

            try:
                file_id = str(file.id)
                file_name = file.name
                mime_type = file.mime_type
                modified_time = file.last_modified

                metadata, file_data = dbx.files_download(file_id)  # type: ignore
                # logger.debug("🔥 Filedata :", file_data.content)
                file_data = BytesIO(file_data.content)

                # Check if the file already exists in the storage
                if check_file_exists(brain_id, file_name):
                    logger.debug("🔥 File already exists in the storage: %s", file_name)

                    self.storage.remove_file(brain_id + "/" + file_name)
                    BrainsVectors().delete_file_from_brain(brain_id, file_name)

                # Check if the file extension is compatible
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
                    logger.info("File is not compatible: %s", file_name)
                    continue

                to_upload_file = UploadFile(
                    file=file_data,
                    filename=file_name,
                )

                # Check if the file already exists in the database
                existing_files = self.sync_files_repo.get_sync_files(sync_active_id)
                existing_file = next(
                    (f for f in existing_files if f.path == file_name), None
                )

                supported = False
                if (existing_file and existing_file.supported) or not existing_file:
                    supported = True
                    await upload_file(
                        to_upload_file,
                        brain_id,
                        current_user,
                        bulk_id,
                        "DropBox",
                        file.web_view_link,
                        notification_id=file.notification_id,
                    )

                if existing_file:
                    # Update the existing file record
                    self.sync_files_repo.update_sync_file(
                        existing_file.id,
                        SyncFileUpdateInput(
                            last_modified=modified_time,
                            supported=supported,
                        ),
                    )
                else:
                    # Create a new file record
                    self.sync_files_repo.create_sync_file(
                        SyncFileInput(
                            path=file_name,
                            syncs_active_id=sync_active_id,
                            last_modified=modified_time,
                            brain_id=brain_id,
                            supported=supported,
                        )
                    )

                downloaded_files.append(file_name)

            except Exception as error:
                logger.error(
                    "An error occurred while downloading DropBox files: %s", error
                )
                # Check if the file already exists in the database
                existing_files = self.sync_files_repo.get_sync_files(sync_active_id)
                existing_file = next(
                    (f for f in existing_files if f.path == file.name), None
                )
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
                            brain_id=brain_id,
                            supported=False,
                        )
                    )
        return {"downloaded_files": downloaded_files}

    async def sync(self, sync_active_id: int, user_id: str):
        """
        Check if the Dropbox sync has not been synced and download the folders and files based on the settings.

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
                    "DropBox sync is not due for sync_active_id: %s", sync_active_id
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
        if sync_user["provider"].lower() != "dropbox":
            logger.warning(
                "Sync provider is not DropBox for sync_active_id: %s", sync_active_id
            )
            return None

        # Download the folders and files from DropBox
        logger.info(
            "Downloading folders and files from Dropbox for sync_active_id: %s",
            sync_active_id,
        )

        # Get the folder id from the settings from sync_active
        settings = sync_active.get("settings", {})
        folders = settings.get("folders", [])
        files_to_download = settings.get("files", [])
        files = []
        files_metadata = []
        if len(folders) > 0:
            files = []
            for folder in folders:
                files.extend(
                    list_dropbox_files(
                        sync_user["credentials"],
                        folder_id=folder,
                        recursive=True,
                    )
                )
        if len(files_to_download) > 0:
            files_metadata = get_dropbox_files_by_id(
                sync_user["credentials"],
                files_to_download,
            )
        files = files + files_metadata  # type: ignore

        if "error" in files:
            logger.error(
                "Failed to download files from DropBox for sync_active_id: %s",
                sync_active_id,
            )
            return None

        # Filter files that have been modified since the last sync
        last_synced_time = (
            datetime.fromisoformat(last_synced).astimezone(timezone.utc)
            if last_synced
            else None
        )
        logger.info("Files retrieved from DropBox: %s", len(files))
        logger.info("Files retrieved from DropBox: %s", files)

        files_to_download = [
            file
            for file in files
            if not file.is_folder
            and (
                (
                    not last_synced_time
                    or datetime.strptime(
                        file.last_modified, "%Y-%m-%d %H:%M:%S"
                    ).replace(tzinfo=timezone.utc)
                    > last_synced_time
                )
                or not check_file_exists(sync_active["brain_id"], file.name)
            )
        ]

        downloaded_files = await self._upload_files(
            sync_user["credentials"],
            files_to_download,
            user_id,
            sync_active["brain_id"],
            sync_active_id,
        )
        if "error" in downloaded_files:
            logger.error(
                "Failed to download files from DropBox for sync_active_id: %s",
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
        logger.info("DropBox sync completed for sync_active_id: %s", sync_active_id)
        return downloaded_files
