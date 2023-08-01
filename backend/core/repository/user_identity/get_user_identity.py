from uuid import UUID

from models.settings import common_dependencies
from models.user_identity import UserIdentity
from repository.user_identity.create_user_identity import create_user_identity


def get_user_identity(user_id: UUID) -> UserIdentity:
    commons = common_dependencies()
    response = (
        commons["supabase"]
        .from_("user_identity")
        .select("*")
        .filter("user_id", "eq", user_id)
        .execute()
    )

    if len(response.data) == 0:
        return create_user_identity(UserIdentity(user_id=user_id))

    return UserIdentity(**response.data[0])
