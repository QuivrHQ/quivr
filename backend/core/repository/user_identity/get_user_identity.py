from uuid import UUID

from models.user_identity import UserIdentity
from repository.user_identity.create_user_identity import create_user_identity

from backend.core.models.settings import get_supabase_client


def get_user_identity(user_id: UUID) -> UserIdentity:
    supabase_client = get_supabase_client()
    response = (
        supabase_client.from_("user_identity")
        .select("*")
        .filter("user_id", "eq", user_id)
        .execute()
    )

    if len(response.data) == 0:
        return create_user_identity(UserIdentity(user_id=user_id))

    return UserIdentity(**response.data[0])
