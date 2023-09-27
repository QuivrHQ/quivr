from uuid import UUID

from models.settings import get_supabase_db


def delete_brain_user(user_id: UUID, brain_id: UUID) -> None:
    supabase_db = get_supabase_db()
    supabase_db.delete_brain_user_by_id(
        user_id=user_id,
        brain_id=brain_id,
    )
