from uuid import UUID

from models.settings import common_dependencies
from repository.brain.get_default_user_brain import get_user_default_brain


def set_as_default_brain_for_user(user_id: UUID, brain_id: UUID):
    commons = common_dependencies()

    old_default_brain = get_user_default_brain(user_id)

    if old_default_brain is not None:
        commons["supabase"].table("brains_users").update(
            {"default_brain": False}
        ).match({"brain_id": old_default_brain.brain_id, "user_id": user_id}).execute()

    commons["supabase"].table("brains_users").update({"default_brain": True}).match(
        {"brain_id": brain_id, "user_id": user_id}
    ).execute()
