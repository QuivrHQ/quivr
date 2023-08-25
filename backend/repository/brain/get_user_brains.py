from uuid import UUID

from models import BrainEntity, get_supabase_db


def get_user_brains(user_id: UUID) -> list[BrainEntity]:
    supabase_db = get_supabase_db()
    results = supabase_db.get_user_brains(user_id)  # type: ignore

    return results  # type: ignore
