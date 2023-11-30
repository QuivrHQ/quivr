from uuid import UUID

from models import get_supabase_db
from modules.brain.entity.brain_entity import MinimalUserBrainEntity


def get_user_brains(user_id: UUID) -> list[MinimalUserBrainEntity]:
    supabase_db = get_supabase_db()
    results = supabase_db.get_user_brains(user_id)  # type: ignore

    return results  # type: ignore
