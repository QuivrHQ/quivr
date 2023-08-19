from uuid import UUID

from models.brain_entity import MinimalBrainEntity
from models.settings import get_supabase_db


def get_brain_for_user(user_id: UUID, brain_id: UUID) -> MinimalBrainEntity:
    supabase_db = get_supabase_db()
    return supabase_db.get_brain_for_user(user_id, brain_id)
