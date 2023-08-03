from uuid import UUID

from models.brain_entity import BrainEntity
from models.databases.supabase.brains import BrainUpdatableProperties
from models.settings import get_supabase_db


def update_brain_by_id(brain_id: UUID, brain: BrainUpdatableProperties) -> BrainEntity:
    """Update a prompt by id"""
    supabase_db = get_supabase_db()

    return supabase_db.update_brain_by_id(brain_id, brain)
