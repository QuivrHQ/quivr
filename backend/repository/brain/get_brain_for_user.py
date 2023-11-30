from uuid import UUID

from models import MinimalUserBrainEntity, get_supabase_db


def get_brain_for_user(user_id: UUID, brain_id: UUID) -> MinimalUserBrainEntity | None:
    supabase_db = get_supabase_db()
    return supabase_db.get_brain_for_user(user_id, brain_id)  # type: ignore
