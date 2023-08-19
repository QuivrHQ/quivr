from models.brain_entity import BrainEntity
from models.databases.supabase.brains import CreateBrainProperties
from models.users import User
from repository.brain.create_brain import create_brain
from repository.brain.create_brain_user import create_brain_user
from repository.brain.get_default_user_brain import get_user_default_brain
from routes.authorizations.types import RoleEnum


def get_default_user_brain_or_create_new(user: User) -> BrainEntity:
    default_brain = get_user_default_brain(user.id)

    if not default_brain:
        default_brain = create_brain(CreateBrainProperties())
        create_brain_user(user.id, default_brain.brain_id, RoleEnum.Owner, True)

    return default_brain
