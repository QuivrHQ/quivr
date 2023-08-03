from uuid import UUID

from models.brain_entity import BrainEntity
from models.settings import common_dependencies


def get_brain_by_id(brain_id: UUID) -> BrainEntity | None:
    commons = common_dependencies()

    return commons["db"].get_brain_by_id(brain_id)
