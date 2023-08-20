from uuid import UUID

from models import get_supabase_client, UserIdentity
from repository.user_identity.create_user_identity import create_user_identity


def get_user_identity(user_id: UUID) -> UserIdentity:
    supabase_client = get_supabase_client()
    response = (
        supabase_client.from_("user_identity")
        .select("*")
        .filter("user_id", "eq", str(user_id))
        .execute()
    )

    if len(response.data) == 0:
        return create_user_identity(UserIdentity(user_id=user_id))

    return UserIdentity(**response.data[0])
