import json

from logger import get_logger
from models.settings import get_supabase_client
from modules.sync.dto.inputs import SyncsUserInput, SyncUserUpdateInput
from modules.sync.repository.sync_interfaces import SyncInterface

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
