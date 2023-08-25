from uuid import UUID

from models import BrainEntity, get_supabase_db
from models.databases.supabase.brains import BrainUpdatableProperties


def update_brain_by_id(brain_id: UUID, brain: BrainUpdatableProperties) -> BrainEntity:
    """Update a prompt by id"""
    supabase_db = get_supabase_db()

    return supabase_db.update_brain_by_id(brain_id, brain)  # type: ignore
