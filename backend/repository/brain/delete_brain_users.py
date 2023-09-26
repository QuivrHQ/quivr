from uuid import UUID

from models.settings import get_supabase_db


def delete_brain_users(brain_id: UUID) -> None:
    supabase_db = get_supabase_db()
    supabase_db.delete_brain_subscribers(
        brain_id=brain_id,
    )
