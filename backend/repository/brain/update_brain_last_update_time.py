from uuid import UUID

from models.settings import get_supabase_db


def update_brain_last_update_time(brain_id: UUID):
    supabase_db = get_supabase_db()
    supabase_db.update_brain_last_update_time(brain_id)
