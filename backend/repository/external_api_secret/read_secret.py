from uuid import UUID

from models import get_supabase_client

from repository.external_api_secret.utils import build_secret_unique_name


def read_secret(
    user_id: UUID,
    brain_id: UUID,
    secret_name: str,
) -> UUID | None:
    supabase_client = get_supabase_client()
    response = supabase_client.rpc(
        "read_secret",
        {
            "secret_name": build_secret_unique_name(
                user_id=user_id, brain_id=brain_id, secret_name=secret_name
            ),
        },
    ).execute()

    return response.data
