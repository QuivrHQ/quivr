from datetime import datetime
from typing import Optional
from uuid import UUID

from models.settings import get_supabase_client
from modules.api_key.entity.api_key import ApiKey
from modules.api_key.repository.api_key_interface import ApiKeysInterface


class ApiKeys(ApiKeysInterface):
    def __init__(self):
        supabase_client = get_supabase_client()
        self.db = supabase_client  # type: ignore

    def create_api_key(
        self, new_key_id, new_api_key, user_id, name, days=30, only_chat=False
    ) -> Optional[ApiKey]:
        response = (
            self.db.table("api_keys")
            .insert(
                [
                    {
                        "key_id": str(new_key_id),
                        "user_id": str(user_id),
                        "api_key": str(new_api_key),
                        "name": str(name),
                        "days": int(days),
                        "only_chat": bool(only_chat),
                        "creation_time": datetime.utcnow().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "is_active": True,
                    }
                ]
            )
            .execute()
        )
        if len(response.data) == 0:
            return None
        return ApiKey(**response.data[0])

    def delete_api_key(self, key_id: str, user_id: UUID):
        return (
            self.db.table("api_keys")
            .update(
                {
                    "is_active": False,
                    "deleted_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                }
            )
            .match({"key_id": key_id, "user_id": user_id})
            .execute()
        )

    def get_active_api_key(self, api_key: str):
        response = (
            self.db.table("api_keys")
            .select("api_key", "creation_time")
            .filter("api_key", "eq", api_key)
            .filter("is_active", "eq", str(True))
            .execute()
        )
        return response

    def get_user_id_by_api_key(self, api_key: str):
        response = (
            self.db.table("api_keys")
            .select("user_id")
            .filter("api_key", "eq", api_key)
            .execute()
        )
        return response

    def get_user_api_keys(self, user_id):
        response = (
            self.db.table("api_keys")
            .select("key_id, creation_time")
            .filter("user_id", "eq", user_id)
            .filter("is_active", "eq", True)
            .execute()
        )
        return response.data
