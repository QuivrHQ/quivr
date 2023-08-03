from uuid import UUID

from models.brain_entity import BrainEntity
from models.settings import common_dependencies


def get_user_brains(user_id: UUID) -> list[BrainEntity]:
    commons = common_dependencies()
    results = commons["db"].get_user_brains(user_id)

    return results
