from typing import Optional
from uuid import UUID

from models.settings import get_supabase_client
from modules.user.entity.user_identity import UserIdentity
from modules.user.repository import create_user_identity
from pydantic import BaseModel


class UserUpdatableProperties(BaseModel):
    openai_api_key: Optional[str]


def update_user_properties(
    user_id: UUID,
    user_identity_updatable_properties: UserUpdatableProperties,
) -> UserIdentity:
    supabase_client = get_supabase_client()
    response = (
        supabase_client.from_("user_identity")
        .update(user_identity_updatable_properties.__dict__)
        .filter("user_id", "eq", user_id)  # type: ignore
        .execute()
    )

    if len(response.data) == 0:
        return create_user_identity(
            user_id, openai_api_key=user_identity_updatable_properties.openai_api_key
        )

    user_identity = response.data[0]
    openai_api_key = user_identity["openai_api_key"]

    return UserIdentity(id=user_id, openai_api_key=openai_api_key)
