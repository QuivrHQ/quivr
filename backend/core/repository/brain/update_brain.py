from uuid import UUID

from models.brain_entity import BrainEntity
from models.databases.supabase.brains import BrainUpdatableProperties
from models.settings import common_dependencies


def update_brain_by_id(brain_id: UUID, brain: BrainUpdatableProperties) -> BrainEntity:
    """Update a prompt by id"""
    commons = common_dependencies()

    return commons["db"].update_brain_by_id(brain_id, brain)
