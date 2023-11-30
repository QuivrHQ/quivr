from uuid import UUID

from models.settings import get_supabase_db
from modules.brain.entity.brain_entity import BrainUser


def get_brain_users(brain_id: UUID) -> list[BrainUser]:
    supabase_db = get_supabase_db()

    return supabase_db.get_brain_users(brain_id)
