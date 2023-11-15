from typing import Optional
from uuid import UUID

from models import get_supabase_client
from modules.user.entity.user_identity import UserIdentity


def create_user_identity(id: UUID, openai_api_key: Optional[str]) -> UserIdentity:
    supabase_client = get_supabase_client()

    response = (
        supabase_client.from_("user_identity")
        .insert(
            {
                "user_id": str(id),
                "openai_api_key": openai_api_key,
            }
        )
        .execute()
    )
    user_identity = response.data[0]
    return UserIdentity(
        id=user_identity.get("user_id"), openai_api_key=user_identity.get("openai_api_key")  # type: ignore
    )
