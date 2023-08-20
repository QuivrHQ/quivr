from uuid import UUID

from models import BrainEntity, get_supabase_db


def get_brain_by_id(brain_id: UUID) -> BrainEntity | None:
    supabase_db = get_supabase_db()

    return supabase_db.get_brain_by_id(brain_id)
