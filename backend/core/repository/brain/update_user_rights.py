from uuid import UUID

from models.settings import common_dependencies


def update_brain_user_rights(brain_id: UUID, user_id: UUID, rights: str) -> None:
    commons = common_dependencies()

    commons["supabase"].table("brains_users").update({"rights": rights}).eq(
        "brain_id",
        brain_id,
    ).eq("user_id", user_id).execute()
