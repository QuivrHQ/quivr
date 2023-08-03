from uuid import UUID

from models.settings import common_dependencies
from routes.authorizations.types import RoleEnum


def create_brain_user(
    user_id: UUID, brain_id: UUID, rights: RoleEnum, is_default_brain: bool
) -> None:
    commons = common_dependencies()
    commons["db"].create_brain_user(
        user_id=user_id,
        brain_id=brain_id,
        rights=rights,
        default_brain=is_default_brain,
    ).data[0]
