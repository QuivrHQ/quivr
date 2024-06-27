from uuid import UUID

from quivr_api.models.settings import get_supabase_client
from quivr_api.modules.brain.repository.interfaces.external_api_secrets_interface import (
    ExternalApiSecretsInterface,
)


def build_secret_unique_name(user_id: UUID, brain_id: UUID, secret_name: str):
    return f"{user_id}-{brain_id}-{secret_name}"


class ExternalApiSecrets(ExternalApiSecretsInterface):
    def __init__(self):
        supabase_client = get_supabase_client()
        self.db = supabase_client

    def create_secret(
        self, user_id: UUID, brain_id: UUID, secret_name: str, secret_value
    ) -> UUID | None:
        response = self.db.rpc(
            "insert_secret",
            {
                "name": build_secret_unique_name(
                    user_id=user_id, brain_id=brain_id, secret_name=secret_name
                ),
                "secret": secret_value,
            },
        ).execute()

        return response.data

    def read_secret(
        self,
        user_id: UUID,
        brain_id: UUID,
        secret_name: str,
    ) -> UUID | None:
        response = self.db.rpc(
            "read_secret",
            {
                "secret_name": build_secret_unique_name(
                    user_id=user_id, brain_id=brain_id, secret_name=secret_name
                ),
            },
        ).execute()

        return response.data

    def delete_secret(self, user_id: UUID, brain_id: UUID, secret_name: str) -> bool:
        response = self.db.rpc(
            "delete_secret",
            {
                "secret_name": build_secret_unique_name(
                    user_id=user_id, brain_id=brain_id, secret_name=secret_name
                ),
            },
        ).execute()

        return response.data
