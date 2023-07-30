from uuid import UUID

from models.settings import common_dependencies


def get_user_email_by_user_id(user_id: UUID) -> str:
    commons = common_dependencies()
    response = (
        commons["supabase"]
        .rpc("get_user_email_by_user_id", {"user_id": user_id})
        .execute()
    )
    return response.data[0]["email"]
