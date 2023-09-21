from uuid import UUID

from models import BrainEntity, get_supabase_db
from models.databases.supabase.brains import BrainUpdatableProperties

from repository.brain.update_brain_last_update_time import update_brain_last_update_time


def update_brain_by_id(brain_id: UUID, brain: BrainUpdatableProperties) -> BrainEntity:
    """Update a prompt by id"""
    supabase_db = get_supabase_db()

    brain_update_answer = supabase_db.update_brain_by_id(brain_id, brain)
    if brain_update_answer is None:
        raise Exception("Brain not found")

    update_brain_last_update_time(brain_id)
    return brain_update_answer
