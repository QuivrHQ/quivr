import json
import os
from datetime import datetime, timedelta
from io import BytesIO
from typing import List
from uuid import UUID

from celery_worker import process_file_and_notify
from fastapi import HTTPException, UploadFile
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from logger import get_logger
from models.settings import get_supabase_client
from modules.brain.entity.brain_entity import RoleEnum
from modules.brain.service.brain_authorization_service import (
    validate_brain_authorization,
)
from modules.knowledge.dto.inputs import CreateKnowledgeProperties
from modules.knowledge.service.knowledge_service import KnowledgeService
from modules.notification.dto.inputs import (
    CreateNotification,
    NotificationUpdatableProperties,
)
from modules.notification.entity.notification import NotificationsStatusEnum
from modules.notification.service.notification_service import NotificationService
from modules.sync.dto.inputs import (
    SyncsActiveInput,
    SyncsActiveUpdateInput,
    SyncsUserInput,
    SyncUserUpdateInput,
)
from modules.sync.entity.sync import SyncsActive
from modules.sync.repository.sync_interfaces import SyncInterface
from modules.upload.service.upload_file import upload_file_storage
from modules.user.service.user_usage import UserUsage
from packages.files.file import convert_bytes, get_file_size
from packages.utils.telemetry import maybe_send_telemetry

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

    def create_sync_user(
        self,
        sync_user_input: SyncsUserInput,
    ):
        """
        Create a new sync user in the database.

        Args:
            sync_user_input (SyncsUserInput): The input data for creating a sync user.

        Returns:
            dict or None: The created sync user data or None if creation failed.
        """
        logger.info("Creating sync user with input: %s", sync_user_input)
        response = (
            self.db.from_("syncs_user")
            .insert(
                {
                    "user_id": sync_user_input.user_id,
                    "provider": sync_user_input.provider,
                    "credentials": sync_user_input.credentials,
                    "state": sync_user_input.state,
                    "name": sync_user_input.name,
                }
            )
            .execute()
        )
        if response.data:
            logger.info("Sync user created successfully: %s", response.data[0])
            return response.data[0]
        logger.warning("Failed to create sync user")
        return None

    def get_syncs_user(self, user_id: str, sync_user_id: int = None):
        """
        Retrieve sync users from the database.

        Args:
            user_id (str): The user ID to filter sync users.
            sync_user_id (int, optional): The sync user ID to filter sync users. Defaults to None.

        Returns:
            list: A list of sync users matching the criteria.
        """
        logger.info(
            "Retrieving sync users for user_id: %s, sync_user_id: %s",
            user_id,
            sync_user_id,
        )
        query = self.db.from_("syncs_user").select("*").eq("user_id", user_id)
        if sync_user_id:
            query = query.eq("id", sync_user_id)
        response = query.execute()
        if response.data:
            logger.info("Sync users retrieved successfully: %s", response.data)
            return response.data
        logger.warning(
            "No sync users found for user_id: %s, sync_user_id: %s",
            user_id,
            sync_user_id,
        )
        return []

    def get_sync_user_by_state(self, state: dict):
        """
        Retrieve a sync user by their state.

        Args:
            state (dict): The state to filter sync users.

        Returns:
            dict or None: The sync user data matching the state or None if not found.
        """
        logger.info("Getting sync user by state: %s", state)

        state_str = json.dumps(state)
        response = (
            self.db.from_("syncs_user").select("*").eq("state", state_str).execute()
        )
        if response.data:
            logger.info("Sync user found by state: %s", response.data[0])
            return response.data[0]
        logger.warning("No sync user found for state: %s", state)
        return []

    def delete_sync_user(self, provider: str, user_id: str):
        """
        Delete a sync user from the database.

        Args:
            provider (str): The provider of the sync user.
            user_id (str): The user ID of the sync user.
        """
        logger.info(
            "Deleting sync user with provider: %s, user_id: %s", provider, user_id
        )
        self.db.from_("syncs_user").delete().eq("provider", provider).eq(
            "user_id", user_id
        ).execute()
        logger.info("Sync user deleted successfully")

    def update_sync_user(
        self, sync_user_id: str, state: dict, sync_user_input: SyncUserUpdateInput
    ):
        """
        Update a sync user in the database.

        Args:
            sync_user_id (str): The user ID of the sync user.
            state (dict): The state to filter sync users.
            sync_user_input (SyncUserUpdateInput): The input data for updating the sync user.
        """
        logger.info(
            "Updating sync user with user_id: %s, state: %s, input: %s",
            sync_user_id,
            state,
            sync_user_input,
        )

        state_str = json.dumps(state)
        self.db.from_("syncs_user").update(sync_user_input.model_dump()).eq(
            "user_id", sync_user_id
        ).eq("state", state_str).execute()
        logger.info("Sync user updated successfully")

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

    def get_google_drive_files(self, credentials: dict, folder_id: str = None):
        """
        Retrieve files from Google Drive.

        Args:
            credentials (dict): The credentials for accessing Google Drive.
            folder_id (str, optional): The folder ID to filter files. Defaults to None.

        Returns:
            dict: A dictionary containing the list of files or an error message.
        """
        logger.info("Retrieving Google Drive files with folder_id: %s", folder_id)
        creds = Credentials.from_authorized_user_info(credentials)
        if creds.expired and creds.refresh_token:
            creds.refresh(GoogleRequest())
            logger.info("Google Drive credentials refreshed")
            # Updating the credentials in the database

        try:
            service = build("drive", "v3", credentials=creds)
            query = f"'{folder_id}' in parents" if folder_id else None
            results = (
                service.files()
                .list(
                    q=query,
                    pageSize=10,
                    fields="nextPageToken, files(id, name, mimeType)",
                )
                .execute()
            )
            items = results.get("files", [])

            if not items:
                logger.info("No files found in Google Drive")
                return {"files": "No files found."}

            files = [
                {
                    "name": item["name"],
                    "id": item["id"],
                    "is_folder": item["mimeType"]
                    == "application/vnd.google-apps.folder",
                }
                for item in items
            ]
            logger.info("Google Drive files retrieved successfully: %s", files)
            return {"files": files}
        except HttpError as error:
            logger.error(
                "An error occurred while retrieving Google Drive files: %s", error
            )
            return {"error": f"An error occurred: {error}"}

    async def download_google_drive_files(
        self, credentials: dict, file_ids: list, current_user: str
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
                # Get file metadata to retrieve the file name
                file_metadata = (
                    service.files().get(fileId=file_id, fields="name").execute()
                )
                file_name = file_metadata["name"]

                request = service.files().get_media(fileId=file_id)
                file_data = request.execute()

                to_upload_file = UploadFile(
                    file=BytesIO(file_data),
                    filename=file_name,
                )

                # Since 'await' is only allowed in asynchronous functions, we need to ensure this function is asynchronous.
                # If the function is not already asynchronous, we should make it so.
                # Assuming the function is now asynchronous:
                await upload_file(
                    to_upload_file, "40ba47d7-51b2-4b2a-9247-89e29619efb0", current_user
                )

                downloaded_files.append(file_name)
                logger.info("File downloaded and saved successfully: %s", file_name)
            return {"downloaded_files": downloaded_files}
        except HttpError as error:
            logger.error(
                "An error occurred while downloading Google Drive files: %s", error
            )
            return {"error": f"An error occurred: {error}"}

    def get_files_folder_user_sync(
        self, sync_active_id: int, user_id: str, folder_id: str = None
    ):
        """
        Retrieve files from a user's sync folder, either from Google Drive or Azure.

        Args:
            sync_active_id (int): The ID of the active sync.
            user_id (str): The user ID associated with the active sync.
            folder_id (str, optional): The folder ID to filter files. Defaults to None.

        Returns:
            dict or str: A dictionary containing the list of files or a string indicating the sync provider.
        """
        logger.info(
            "Retrieving files for user sync with sync_active_id: %s, user_id: %s, folder_id: %s",
            sync_active_id,
            user_id,
            folder_id,
        )

        # Check whether the sync is Google or Azure
        sync_user = self.get_syncs_user(user_id=user_id, sync_user_id=sync_active_id)
        if not sync_user:
            logger.warning(
                "No sync user found for sync_active_id: %s, user_id: %s",
                sync_active_id,
                user_id,
            )
            return None

        sync_user = sync_user[0]
        logger.info("Sync user found: %s", sync_user)

        provider = sync_user["provider"].lower()
        if provider == "google":
            logger.info("Getting files for Google sync")
            return self.get_google_drive_files(sync_user["credentials"], folder_id)
        elif provider == "azure":
            logger.info("Getting files for Azure sync")
            return "Azure"
        else:
            logger.warning("No sync found for provider: %s", sync_user["provider"])
            return "No sync found"

    async def get_syncs_active_in_interval(self):
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
            .lt("last_synced", (current_time - timedelta(minutes=1)).isoformat())
            .execute()
        )
        if response.data:
            logger.info("Active syncs retrieved successfully: %s", response.data)
            for sync in response.data:
                # Now we can call the sync_google_drive_if_not_synced method to sync the Google Drive files
                await self.sync_google_drive_if_not_synced(sync["id"], sync["user_id"])

            return response.data
        logger.warning("No active syncs found due for synchronization")
        return []

    async def sync_google_drive_if_not_synced(self, sync_active_id: int, user_id: str):
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
        sync_active = self.get_details_sync_active(sync_active_id)
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
        sync_user = self.get_syncs_user(
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
        downloaded_files = await self.download_google_drive_files(
            sync_user["credentials"], file_ids, user_id
        )
        if "error" in downloaded_files:
            logger.error(
                "Failed to download files from Google Drive for sync_active_id: %s",
                sync_active_id,
            )
            return None

        # Update the last_synced timestamp
        self.update_sync_active(
            sync_active_id,
            SyncsActiveUpdateInput(last_synced=datetime.now().isoformat()),
        )
        logger.info(
            "Google Drive sync completed for sync_active_id: %s", sync_active_id
        )
        return downloaded_files


async def upload_file(
    upload_file: UploadFile,
    brain_id: UUID,
    current_user: str,
):
    validate_brain_authorization(
        brain_id, current_user, [RoleEnum.Editor, RoleEnum.Owner]
    )
    user_daily_usage = UserUsage(
        id=current_user,
    )
    upload_notification = notification_service.add_notification(
        CreateNotification(
            user_id=current_user,
            status=NotificationsStatusEnum.INFO,
            title=f"Processing File {upload_file.filename}",
        )
    )

    user_settings = user_daily_usage.get_user_settings()

    remaining_free_space = user_settings.get("max_brain_size", 1000000000)
    maybe_send_telemetry("upload_file", {"file_name": upload_file.filename})
    file_size = get_file_size(upload_file)
    if remaining_free_space - file_size < 0:
        message = f"Brain will exceed maximum capacity. Maximum file allowed is : {convert_bytes(remaining_free_space)}"
        raise HTTPException(status_code=403, detail=message)

    file_content = await upload_file.read()

    filename_with_brain_id = str(brain_id) + "/" + str(upload_file.filename)

    try:
        file_in_storage = upload_file_storage(file_content, filename_with_brain_id)

    except Exception as e:
        print(e)

        notification_service.update_notification_by_id(
            upload_notification.id if upload_notification else None,
            NotificationUpdatableProperties(
                status=NotificationsStatusEnum.ERROR,
                description=f"There was an error uploading the file: {e}",
            ),
        )
        if "The resource already exists" in str(e):
            raise HTTPException(
                status_code=403,
                detail=f"File {upload_file.filename} already exists in storage.",
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to upload file to storage. {e}"
            )

    knowledge_to_add = CreateKnowledgeProperties(
        brain_id=brain_id,
        file_name=upload_file.filename,
        extension=os.path.splitext(
            upload_file.filename  # pyright: ignore reportPrivateUsage=none
        )[-1].lower(),
    )

    added_knowledge = knowledge_service.add_knowledge(knowledge_to_add)

    process_file_and_notify.delay(
        file_name=filename_with_brain_id,
        file_original_name=upload_file.filename,
        brain_id=brain_id,
        notification_id=upload_notification.id,
    )
    return {"message": "File processing has started."}
