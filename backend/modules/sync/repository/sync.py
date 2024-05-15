import json
import os
from typing import List

from logger import get_logger
from models.settings import get_supabase_client
from modules.sync.dto.inputs import SyncsUserInput, SyncUserUpdateInput
from modules.sync.repository.sync_interfaces import SyncInterface
from modules.sync.dto.inputs import SyncsActiveInput, SyncsActiveUpdateInput
from modules.sync.entity.sync import SyncsActive
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = get_logger(__name__)


class Sync(SyncInterface):
    def __init__(self):
        supabase_client = get_supabase_client()
        self.db = supabase_client  # type: ignore

    def create_sync_user(
        self,
        sync_user_input: SyncsUserInput,
    ):
        logger.info("Creating sync user")
        logger.info(sync_user_input)
        response = (
            self.db.from_("syncs_user")
            .insert(
                {
                    "user_id": sync_user_input.user_id,
                    "sync_name": sync_user_input.sync_name,
                    "credentials": sync_user_input.credentials,
                    "state": sync_user_input.state,
                }
            )
            .execute()
        )
        if response.data:
            return response.data[0]
        return None

    def get_syncs_user(self, user_id: str):
        response = (
            self.db.from_("syncs_user").select("*").eq("user_id", user_id).execute()
        )
        if response.data:
            return response.data

        return []

    def get_sync_user_by_state(self, state: dict):
        logger.info("Getting sync user by state")
        logger.info(state)

        state_str = json.dumps(state)
        response = (
            self.db.from_("syncs_user").select("*").eq("state", state_str).execute()
        )
        if response.data:
            return response.data[0]

        return []

    def delete_sync_user(self, sync_name: str, user_id: str):
        self.db.from_("syncs_user").delete().eq("sync_name", sync_name).eq(
            "user_id", user_id
        ).execute()

    def update_sync_user(
        self, sync_user_id: str, state: dict, sync_user_input: SyncUserUpdateInput
    ):
        logger.info("Updating sync user")
        logger.info(sync_user_input)

        state_str = json.dumps(state)
        self.db.from_("syncs_user").update(sync_user_input.model_dump()).eq(
            "user_id", sync_user_id
        ).eq("state", state_str).execute()

    def create_sync_active(self, sync_active_input: SyncsActiveInput) -> SyncsActive:
        response = (
            self.db.from_("syncs_active")
            .insert(sync_active_input.model_dump())
            .execute()
        )
        if response.data:
            return SyncsActive(**response.data[0])
        return None

    def get_syncs_active(self, user_id: str) -> List[SyncsActive]:
        response = (
            self.db.from_("syncs_active").select("*").eq("user_id", user_id).execute()
        )
        if response.data:
            return [SyncsActive(**sync) for sync in response.data]
        return []

    def update_sync_active(
        self, sync_id: str, sync_active_input: SyncsActiveUpdateInput
    ):
        response = (
            self.db.from_("syncs_active")
            .update(sync_active_input.model_dump())
            .eq("id", sync_id)
            .execute()
        )
        if response.data:
            return response.data[0]
        return None

    def delete_sync_active(self, sync_active_id: int, user_id: str):
        response = (
            self.db.from_("syncs_active")
            .delete()
            .eq("id", sync_active_id)
            .eq("user_id", user_id)
            .execute()
        )
        if response.data:
            return response.data[0]
        return None

    def get_details_sync_active(self, sync_active_id: int):
        # Get the syncs_user connect to the syncs_active via the syncs_user_id key
        response = (
            self.db.table("syncs_active")
            .select("*, syncs_user(sync_name, credentials)")
            .eq("id", sync_active_id)
            .execute()
        )
        if response.data:
            logger.info("Getting details sync active")
            logger.info(response.data)
            return response.data[0]
        return None

    def get_google_drive_files(self, credentials: dict, folder_id: str = None):
        creds = Credentials.from_authorized_user_info(credentials)
        if creds.expired and creds.refresh_token:
            creds.refresh(GoogleRequest())
        
        try:
            service = build("drive", "v3", credentials=creds)
            query = f"'{folder_id}' in parents" if folder_id else None
            results = (
                service.files()
                .list(q=query, pageSize=10, fields="nextPageToken, files(id, name, mimeType)")
                .execute()
            )
            items = results.get("files", [])

            if not items:
                return {"files": "No files found."}

            files = [{"name": item["name"], "id": item["id"], "is_folder": item["mimeType"] == "application/vnd.google-apps.folder"} for item in items]
            return {"files": files}
        except HttpError as error:
            logger.error(f"An error occurred: {error}")
            return {"error": f"An error occurred: {error}"}

    def get_files_folder_active_sync(self, sync_active_id: str, folder_id: str = None):
        ## Check whether the sync is google or azure
        sync_active = self.get_details_sync_active(sync_active_id)
        logger.info(sync_active)
        if sync_active["syncs_user"]["sync_name"].lower() == "google":
            logger.info("Getting files for google sync")
            return self.get_google_drive_files(sync_active["syncs_user"]["credentials"], folder_id)
        if sync_active["syncs_user"]["sync_name"].lower() == "azure":
            logger.info("Getting files for azure sync")
            return "Azure"
        return "No sync found"
