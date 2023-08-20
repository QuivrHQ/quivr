from uuid import UUID

from models import get_supabase_client


def update_brain_user_rights(brain_id: UUID, user_id: UUID, rights: str) -> None:
    supabase_client = get_supabase_client()

    supabase_client.table("brains_users").update({"rights": rights}).eq(
        "brain_id",
        brain_id,
    ).eq("user_id", user_id).execute()
