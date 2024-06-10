import os
from datetime import datetime, timedelta, timezone
from io import BytesIO

import msal
import requests
from fastapi import HTTPException, UploadFile
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
from modules.sync.utils.list_files import get_azure_files_by_id, list_azure_files
from modules.sync.utils.upload import upload_file
from modules.upload.service.upload_file import check_file_exists
from pydantic import BaseModel, ConfigDict

logger = get_logger(__name__)

CLIENT_ID = os.getenv("SHAREPOINT_CLIENT_ID")
AUTHORITY = "https://login.microsoftonline.com/common"
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5050")
REDIRECT_URI = f"{BACKEND_URL}/sync/azure/oauth2callback"
SCOPE = [
    "https://graph.microsoft.com/Files.Read",
    "https://graph.microsoft.com/User.Read",
    "https://graph.microsoft.com/Sites.Read.All",
]


class AzureSyncUtils(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    sync_user_service: SyncUserService
    sync_active_service: SyncService
    sync_files_repo: SyncFiles
    storage: Storage

    def get_headers(self, token_data):
        return {
            "Authorization": f"Bearer {token_data['access_token']}",
            "Accept": "application/json",
        }

    def refresh_token(self, refresh_token):
        client = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
        result = client.acquire_token_by_refresh_token(refresh_token, scopes=SCOPE)
        if "access_token" not in result:
            raise HTTPException(status_code=400, detail="Failed to refresh token")
        return result

    async def _upload_files(
        self,
        token_data: dict,
        files: list,
        current_user: str,
        brain_id: str,
        sync_active_id: int,
    ):
        """
        Download files from Azure.

        Args:
            token_data (dict): The token data for accessing Azure.
            files (list): The list of file metadata to download.

        Returns:
            dict: A dictionary containing the status of the download or an error message.
        """
        logger.info("Downloading Azure files with metadata: %s", files)
        headers = self.get_headers(token_data)

        downloaded_files = []
        for file in files:
            try:
                file_id = file["id"]
                file_name = file["name"]
                modified_time = file["last_modified"]

                download_endpoint = (
                    f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/content"
                )
                logger.info("Downloading file: %s", file_name)
                download_response = requests.get(
                    download_endpoint, headers=headers, stream=True
                )
                if download_response.status_code == 401:
                    token_data = self.refresh_token(token_data["refresh_token"])
                    headers = self.get_headers(token_data)
                    download_response = requests.get(
                        download_endpoint, headers=headers, stream=True
                    )
                if download_response.status_code != 200:
                    logger.error("Failed to download file: %s", file_name)
                    continue

                file_data = BytesIO(download_response.content)

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
                    await upload_file(to_upload_file, brain_id, current_user)

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
                    "An error occurred while downloading Azure files: %s", error
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
        Check if the Azure sync has not been synced and download the folders and files based on the settings.

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
                    "Azure sync is not due for sync_active_id: %s", sync_active_id
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
        if sync_user["provider"].lower() != "azure":
            logger.warning(
                "Sync provider is not Azure for sync_active_id: %s", sync_active_id
            )
            return None

        # Download the folders and files from Azure
        logger.info(
            "Downloading folders and files from Azure for sync_active_id: %s",
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
                    list_azure_files(
                        sync_user["credentials"],
                        folder_id=folder,
                        recursive=True,
                    )
                )
        if len(files_to_download) > 0:
            files_metadata = get_azure_files_by_id(
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
        logger.info("Files retrieved from Azure: %s", len(files))
        logger.info("Files retrieved from Azure: %s", files)
        files_to_download = [
            file
            for file in files
            if not file["is_folder"]
            and (
                (
                    not last_synced_time
                    or datetime.strptime(
                        file["last_modified"], "%Y-%m-%dT%H:%M:%SZ"
                    ).replace(tzinfo=timezone.utc)
                    > last_synced_time
                )
                or not check_file_exists(sync_active["brain_id"], file["name"])
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
        logger.info("Azure sync completed for sync_active_id: %s", sync_active_id)
        return downloaded_files


import asyncio


async def main():
    sync_user_service = SyncUserService()
    sync_active_service = SyncService()
    sync_files_repo = SyncFiles()
    storage = Storage()

    azure_sync_utils = AzureSyncUtils(
        sync_user_service=sync_user_service,
        sync_active_service=sync_active_service,
        sync_files_repo=sync_files_repo,
        storage=storage,
    )
    await azure_sync_utils.sync(3, "39418e3b-0258-4452-af60-7acfcc1263ff")


if __name__ == "__main__":
    asyncio.run(main())
