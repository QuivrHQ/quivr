from models.settings import common_dependencies
from models.user_identity import UserIdentity


def create_user_identity(user_identity: UserIdentity) -> UserIdentity:
    commons = common_dependencies()
    user_identity_dict = user_identity.dict()
    user_identity_dict["user_id"] = str(user_identity.user_id)
    response = (
        commons["supabase"].from_("user_identity").insert(user_identity_dict).execute()
    )

    return UserIdentity(**response.data[0])
