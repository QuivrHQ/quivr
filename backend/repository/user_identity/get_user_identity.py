from multiprocessing import get_logger
from uuid import UUID

from models import get_supabase_client, UserIdentity
from repository.user_identity.create_user_identity import create_user_identity

logger = get_logger()


def get_user_identity(user_id: UUID) -> UserIdentity:
    supabase_client = get_supabase_client()
    response = (
        supabase_client.from_("user_identity")
        .select("*")
        .filter("user_id", "eq", str(user_id))
        .execute()
    )

    if len(response.data) == 0:
        return create_user_identity(user_id, openai_api_key=None)

    user_identity = response.data[0]
    openai_api_key = user_identity["openai_api_key"]

    return UserIdentity(id=user_id, openai_api_key=openai_api_key)
