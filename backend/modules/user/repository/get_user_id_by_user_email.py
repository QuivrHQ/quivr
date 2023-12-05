from uuid import UUID

from models import get_supabase_client


def get_user_id_by_user_email(email: str) -> UUID | None:
    supabase_client = get_supabase_client()
    response = (
        supabase_client.rpc("get_user_id_by_user_email", {"user_email": email})
        .execute()
        .data
    )
    if len(response) > 0:
        return response[0]["user_id"]
    return None
