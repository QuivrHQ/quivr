from models.settings import get_supabase_client
from models.user_identity import UserIdentity


def create_user_identity(user_identity: UserIdentity) -> UserIdentity:
    supabase_client = get_supabase_client()
    user_identity_dict = user_identity.dict()
    user_identity_dict["user_id"] = str(user_identity.user_id)
    response = (
        supabase_client.from_("user_identity").insert(user_identity_dict).execute()
    )

    return UserIdentity(**response.data[0])
