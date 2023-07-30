from uuid import UUID

from models.settings import common_dependencies


def get_user_id_by_user_email(email: str) -> UUID:
    commons = common_dependencies()
    response = (
        commons["supabase"]
        .rpc("get_user_id_by_user_email", {"user_email": email})
        .execute()
    )
    return response.data[0]["user_id"]
