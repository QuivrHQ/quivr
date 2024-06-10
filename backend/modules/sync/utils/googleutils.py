from datetime import datetime, timedelta, timezone
from io import BytesIO

from fastapi import UploadFile
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from logger import get_logger
from modules.brain.repository.brains_vectors import BrainsVectors
from modules.knowledge.repository.storage import Storage
from modules.sync.dto.inputs import (
    SyncFileInput,
    SyncFileUpdateInput,
    SyncsActiveUpdateInput,
)
from modules.sync.repository.sync_files import SyncFiles
from modules.sync.service.sync_service import SyncService, SyncUserService
from modules.sync.utils.list_files import (
    get_google_drive_files,
    get_google_drive_files_by_id,
)
from modules.sync.utils.upload import upload_file
from modules.upload.service.upload_file import check_file_exists
from pydantic import BaseModel, ConfigDict

logger = get_logger(__name__)


class GoogleSyncUtils(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    sync_user_service: SyncUserService
    sync_active_service: SyncService
    sync_files_repo: SyncFiles
    storage: Storage

    async def _upload_files(
        self,
        credentials: dict,
        files: list,
        current_user: str,
        brain_id: str,
        sync_active_id: int,
    ):
        """
        Download files from Google Drive.

        Args:
            credentials (dict): The credentials for accessing Google Drive.
            files (list): The list of file metadata to download.

        Returns:
            dict: A dictionary containing the status of the download or an error message.
        """
        logger.info("Downloading Google Drive files with metadata: %s", files)
        creds = Credentials.from_authorized_user_info(credentials)
        if creds.expired and creds.refresh_token:
            creds.refresh(GoogleRequest())
            logger.info("Google Drive credentials refreshed")
            # Updating the credentials in the database

        service = build("drive", "v3", credentials=creds)
        downloaded_files = []
        for file in files:
            logger.info("🔥🔥🔥🔥: %s", file)
            try:
                file_id = file["id"]
                file_name = file["name"]
                mime_type = file["mime_type"]
                modified_time = file["last_modified"]
                # Convert Google Docs files to appropriate formats before downloading
                if mime_type == "application/vnd.google-apps.document":
                    logger.debug(
                        "Converting Google Docs file with file_id: %s to DOCX.",
                        file_id,
                    )
                    request = service.files().export_media(
                        fileId=file_id,
                        mimeType="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    )
                    file_name += ".docx"
                elif mime_type == "application/vnd.google-apps.spreadsheet":
                    logger.debug(
                        "Converting Google Sheets file with file_id: %s to XLSX.",
                        file_id,
                    )
                    request = service.files().export_media(
                        fileId=file_id,
                        mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                    file_name += ".xlsx"
                elif mime_type == "application/vnd.google-apps.presentation":
                    logger.debug(
                        "Converting Google Slides file with file_id: %s to PPTX.",
                        file_id,
                    )
                    request = service.files().export_media(
                        fileId=file_id,
                        mimeType="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    )
                    file_name += ".pptx"
                ### Elif pdf, txt, md, csv, docx, xlsx, pptx, doc
                elif file_name.split(".")[-1] in [
                    "pdf",
                    "txt",
                    "md",
                    "csv",
                    "docx",
                    "xlsx",
                    "pptx",
                    "doc",
                ]:
                    request = service.files().get_media(fileId=file_id)
                else:
                    logger.warning(
                        "Skipping unsupported file type: %s for file_id: %s",
                        mime_type,
                        file_id,
                    )
                    continue

                file_data = request.execute()

                # Check if the file already exists in the storage
                if check_file_exists(brain_id, file_name):
                    logger.debug("🔥 File already exists in the storage: %s", file_name)

                    self.storage.remove_file(brain_id + "/" + file_name)
                    BrainsVectors().delete_file_from_brain(brain_id, file_name)

                to_upload_file = UploadFile(
                    file=BytesIO(file_data),
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
                    await upload_file(to_upload_file, brain_id, current_user)  # type: ignore

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
            except HttpError as error:
                logger.error(
                    "An error occurred while downloading Google Drive files: %s",
                    error,
                )
                # Check if the file already exists in the database
                existing_files = self.sync_files_repo.get_sync_files(sync_active_id)
                existing_file = next(
                    (f for f in existing_files if f.path == file["name"]), None
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
                            path=file["name"],
                            syncs_active_id=sync_active_id,
                            last_modified=file["last_modified"],
                            brain_id=brain_id,
                            supported=False,
                        )
                    )
        return {"downloaded_files": downloaded_files}

    async def sync(self, sync_active_id: int, user_id: str):
        """
        Check if the Google sync has not been synced and download the folders and files based on the settings.

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
                    "Google sync is not due for sync_active_id: %s", sync_active_id
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
        if sync_user["provider"].lower() != "google":
            logger.warning(
                "Sync provider is not Google for sync_active_id: %s", sync_active_id
            )
            return None

        # Download the folders and files from Google Drive
        logger.info(
            "Downloading folders and files from Google Drive for sync_active_id: %s",
            sync_active_id,
        )

        settings = sync_active.get("settings", {})
        folders = settings.get("folders", [])
        files_to_download = settings.get("files", [])
        files = []
        files_metadata = []
        if len(folders) > 0:
            files = []
            for folder in folders:
                files.extend(
                    get_google_drive_files(
                        sync_user["credentials"],
                        folder_id=folder,
                        recursive=True,
                    )
                )
        if len(files_to_download) > 0:
            files_metadata = get_google_drive_files_by_id(
                sync_user["credentials"], files_to_download
            )
        files = files + files_metadata  # type: ignore
        if "error" in files:
            logger.error(
                "Failed to download files from Google Drive for sync_active_id: %s",
                sync_active_id,
            )
            return None

        # Filter files that have been modified since the last sync
        last_synced_time = datetime.fromisoformat(last_synced) if last_synced else None

        files_to_download = [
            file
            for file in files
            if not file["is_folder"]
            and (
                (
                    not last_synced_time
                    or datetime.fromisoformat(file["last_modified"]) > last_synced_time
                )
                or not check_file_exists(sync_active["brain_id"], file["name"])
            )
        ]

        logger.error(files_to_download)

        downloaded_files = await self._upload_files(
            sync_user["credentials"],
            files_to_download,
            user_id,
            sync_active["brain_id"],
            sync_active_id,
        )

        # Update the last_synced timestamp
        self.sync_active_service.update_sync_active(
            sync_active_id,
            SyncsActiveUpdateInput(
                last_synced=datetime.now().astimezone().isoformat(),
                force_sync=False,
            ),
        )
        logger.info(
            "Google Drive sync completed for sync_active_id: %s", sync_active_id
        )
        return downloaded_files


import asyncio


async def main():
    sync_user_service = SyncUserService()
    sync_active_service = SyncService()
    sync_files_repo = SyncFiles()
    storage = Storage()

    google_sync_utils = GoogleSyncUtils(
        sync_user_service=sync_user_service,
        sync_active_service=sync_active_service,
        sync_files_repo=sync_files_repo,
        storage=storage,
    )
    await google_sync_utils.sync(2, "39418e3b-0258-4452-af60-7acfcc1263ff")


if __name__ == "__main__":
    asyncio.run(main())
