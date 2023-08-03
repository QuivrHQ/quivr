from uuid import UUID

from models.settings import get_supabase_client


def get_user_id_by_user_email(email: str) -> UUID:
    supabase_client = get_supabase_client()
    response = supabase_client.rpc(
        "get_user_id_by_user_email", {"user_email": email}
    ).execute()
    return response.data[0]["user_id"]
