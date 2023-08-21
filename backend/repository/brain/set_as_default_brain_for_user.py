from uuid import UUID

from models import get_supabase_client
from repository.brain import get_user_default_brain


def set_as_default_brain_for_user(user_id: UUID, brain_id: UUID):
    supabase_client = get_supabase_client()

    old_default_brain = get_user_default_brain(user_id)

    if old_default_brain is not None:
        supabase_client.table("brains_users").update({"default_brain": False}).match(
            {"brain_id": old_default_brain.brain_id, "user_id": user_id}
        ).execute()

    supabase_client.table("brains_users").update({"default_brain": True}).match(
        {"brain_id": brain_id, "user_id": user_id}
    ).execute()
