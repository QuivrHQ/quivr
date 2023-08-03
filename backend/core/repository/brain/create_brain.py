from models.brain_entity import BrainEntity
from models.databases.supabase.brains import CreateBrainProperties
from models.settings import common_dependencies


def create_brain(brain: CreateBrainProperties) -> BrainEntity:
    commons = common_dependencies()

    return commons["db"].create_brain(brain.dict(exclude_unset=True))
