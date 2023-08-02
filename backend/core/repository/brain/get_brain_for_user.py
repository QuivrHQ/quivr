from uuid import UUID

from models.brain_entity import MinimalBrainEntity
from models.settings import common_dependencies


def get_brain_for_user(user_id: UUID, brain_id: UUID) -> MinimalBrainEntity:
    commons = common_dependencies()
    return commons["db"].get_brain_for_user(user_id, brain_id)
