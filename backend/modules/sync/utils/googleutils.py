from datetime import datetime, timedelta
from io import BytesIO

from fastapi import UploadFile
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from logger import get_logger
from modules.sync.dto.inputs import SyncsActiveUpdateInput
from modules.sync.service.sync_service import SyncService, SyncUserService
from modules.sync.utils.upload import upload_file
from pydantic import BaseModel, ConfigDict
from requests import HTTPError
from modules.sync.utils.list_files import get_google_drive_files

logger = get_logger(__name__)


class GoogleSyncUtils(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    sync_user_service: SyncUserService
    sync_active_service: SyncService

    async def _upload_files(
        self, credentials: dict, file_ids: list, current_user: str, brain_id: str
    ):
        """
        Download files from Google Drive.

        Args:
            credentials (dict): The credentials for accessing Google Drive.
            file_ids (list): The list of file IDs to download.

        Returns:
            dict: A dictionary containing the status of the download or an error message.
        """
        logger.info("Downloading Google Drive files with file_ids: %s", file_ids)
        creds = Credentials.from_authorized_user_info(credentials)
        if creds.expired and creds.refresh_token:
            creds.refresh(GoogleRequest())
            logger.info("Google Drive credentials refreshed")
            # Updating the credentials in the database

        try:
            service = build("drive", "v3", credentials=creds)
            downloaded_files = []
            for file_id in file_ids:
                logger.info("Downloading file with file_id: %s", file_id)
                # Get file metadata to retrieve the file name, mimeType, and modifiedTime
                file_metadata = (
                    service.files()
                    .get(fileId=file_id, fields="name, mimeType, modifiedTime")
                    .execute()
                )
                file_name = file_metadata["name"]
                mime_type = file_metadata["mimeType"]
                modified_time = file_metadata["modifiedTime"]
                logger.info("File last modified on: %s", modified_time)
                # Convert Google Docs files to PDF before downloading
                if mime_type.startswith("application/vnd.google-apps."):
                    logger.info(
                        "Converting Google Docs file with file_id: %s to PDF.", file_id
                    )
                    request = service.files().export_media(
                        fileId=file_id, mimeType="application/pdf"
                    )
                    file_name += ".pdf"
                else:
                    request = service.files().get_media(fileId=file_id)

                file_data = request.execute()

                to_upload_file = UploadFile(
                    file=BytesIO(file_data),
                    filename=file_name,
                )

                # Since 'await' is only allowed in asynchronous functions, we need to ensure this function is asynchronous.
                # If the function is not already asynchronous, we should make it so.
                # Assuming the function is now asynchronous:
                await upload_file(to_upload_file, brain_id, current_user)

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
        files = self.get_google_drive_files(
            sync_user["credentials"], folder_id=folders[0] if folders else None
        )
        if "error" in files:
            logger.error(
                "Failed to download files from Google Drive for sync_active_id: %s",
                sync_active_id,
            )
            return None

        # Download only the files found
        file_ids = [
            file["id"] for file in files.get("files", []) if not file["is_folder"]
        ]
        downloaded_files = await self._upload_files(
            sync_user["credentials"], file_ids, user_id, sync_active["brain_id"]
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
    google_sync_utils = GoogleSyncUtils(
        sync_user_service=sync_user_service, sync_active_service=sync_active_service
    )
    await google_sync_utils.sync(2, "39418e3b-0258-4452-af60-7acfcc1263ff")


if __name__ == "__main__":
    asyncio.run(main())
