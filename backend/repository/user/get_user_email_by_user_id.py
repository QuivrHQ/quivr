from uuid import UUID

from models import get_supabase_client


def get_user_email_by_user_id(user_id: UUID) -> str:
    supabase_client = get_supabase_client()
    response = supabase_client.rpc(
        "get_user_email_by_user_id", {"user_id": user_id}
    ).execute()
    return response.data[0]["email"]
