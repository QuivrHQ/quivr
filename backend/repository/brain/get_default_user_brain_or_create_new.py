from models.databases.supabase.brains import CreateBrainProperties
from models import BrainEntity, User
from routes.authorizations.types import RoleEnum

from repository.brain import (
    create_brain,
    create_brain_user,
    get_user_default_brain
)


def get_default_user_brain_or_create_new(user: User) -> BrainEntity:
    default_brain = get_user_default_brain(user.id)

    if not default_brain:
        default_brain = create_brain(CreateBrainProperties())
        create_brain_user(user.id, default_brain.brain_id, RoleEnum.Owner, True)

    return default_brain
