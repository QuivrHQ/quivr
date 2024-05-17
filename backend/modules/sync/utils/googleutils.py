from datetime import datetime, timedelta
from io import BytesIO

from fastapi import UploadFile
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from logger import get_logger
from modules.sync.dto.inputs import (
    SyncFileInput,
    SyncFileUpdateInput,
    SyncsActiveUpdateInput,
)
from modules.sync.repository.sync_files import SyncFiles
from modules.sync.service.sync_service import SyncService, SyncUserService
from modules.sync.utils.list_files import get_google_drive_files
from modules.sync.utils.upload import upload_file
from pydantic import BaseModel, ConfigDict

logger = get_logger(__name__)


class GoogleSyncUtils(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    sync_user_service: SyncUserService
    sync_active_service: SyncService
    sync_files_repo: SyncFiles

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

        try:
            service = build("drive", "v3", credentials=creds)
            downloaded_files = []
            for file in files:
                file_id = file["id"]
                file_name = file["name"]
                mime_type = file["mime_type"]
                modified_time = file["last_modified"]
                logger.info("Downloading file with file_id: %s", file_id)
                logger.info("File last modified on: %s", modified_time)
                # Convert Google Docs files to appropriate formats before downloading
                if mime_type == "application/vnd.google-apps.document":
                    logger.info(
                        "Converting Google Docs file with file_id: %s to DOCX.", file_id
                    )
                    request = service.files().export_media(
                        fileId=file_id,
                        mimeType="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    )
                    file_name += ".docx"
                elif mime_type == "application/vnd.google-apps.spreadsheet":
                    logger.info(
                        "Converting Google Sheets file with file_id: %s to XLSX.",
                        file_id,
                    )
                    request = service.files().export_media(
                        fileId=file_id,
                        mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                    file_name += ".xlsx"
                elif mime_type == "application/vnd.google-apps.presentation":
                    logger.info(
                        "Converting Google Slides file with file_id: %s to PPTX.",
                        file_id,
                    )
                    request = service.files().export_media(
                        fileId=file_id,
                        mimeType="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    )
                    file_name += ".pptx"
                else:
                    request = service.files().get_media(fileId=file_id)

                file_data = request.execute()

                to_upload_file = UploadFile(
                    file=BytesIO(file_data),
                    filename=file_name,
                )

                await upload_file(to_upload_file, brain_id, current_user)

                # Check if the file already exists in the database
                existing_files = self.sync_files_repo.get_sync_files(sync_active_id)
                existing_file = next(
                    (f for f in existing_files if f.path == file_name), None
                )

                if existing_file:
                    # Update the existing file record
                    self.sync_files_repo.update_sync_file(
                        existing_file.id,
                        SyncFileUpdateInput(
                            last_modified=modified_time.isoformat(),
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
                        )
                    )

                downloaded_files.append(file_name)
                logger.info("File downloaded and saved successfully: %s", file_name)
            return {"downloaded_files": downloaded_files}
        except HttpError as error:
            logger.error(
                "An error occurred while downloading Google Drive files: %s", error
            )
            return {"error": f"An error occurred: {error}"}

    async def sync(self, sync_active_id: int, user_id: str):
        """
        Check if the Google sync has not been synced and download the folders and files based on the settings.

        Args:
            sync_active_id (int): The ID of the active sync.
            user_id (str): The user ID associated with the active sync.
        """
        logger.info(
            "Checking if Google sync has not been synced for sync_active_id: %s, user_id: %s",
            sync_active_id,
            user_id,
        )

        # Retrieve the active sync details
        sync_active = self.sync_active_service.get_details_sync_active(sync_active_id)
        if not sync_active:
            logger.warning(
                "No active sync found for sync_active_id: %s", sync_active_id
            )
            return None

        # Check if the sync is due
        last_synced = sync_active.get("last_synced")
        sync_interval_minutes = sync_active.get("sync_interval_minutes", 0)
        if last_synced:
            last_synced_time = datetime.fromisoformat(last_synced)
            current_time = datetime.now().astimezone()
            if current_time - last_synced_time < timedelta(
                minutes=sync_interval_minutes
            ):
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

        # Get the folder id from the settings from sync_active
        settings = sync_active.get("settings", {})
        folders = settings.get("folders", [])
        logger.info("Folders: %s", folders)
        files = get_google_drive_files(
            sync_user["credentials"], folder_id=folders[0] if folders else None
        )
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
            for file in files.get("files", [])
            if not file["is_folder"]
            and (
                not last_synced_time
                or datetime.fromisoformat(file["last_modified"]) > last_synced_time
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
                "Failed to download files from Google Drive for sync_active_id: %s",
                sync_active_id,
            )
            return None

        # Update the last_synced timestamp
        self.sync_active_service.update_sync_active(
            sync_active_id,
            SyncsActiveUpdateInput(last_synced=datetime.now().isoformat()),
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
    google_sync_utils = GoogleSyncUtils(
        sync_user_service=sync_user_service,
        sync_active_service=sync_active_service,
        sync_files_repo=sync_files_repo,
    )
    await google_sync_utils.sync(2, "39418e3b-0258-4452-af60-7acfcc1263ff")


if __name__ == "__main__":
    asyncio.run(main())
