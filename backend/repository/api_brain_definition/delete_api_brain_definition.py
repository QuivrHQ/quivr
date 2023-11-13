from uuid import UUID

from models.settings import get_supabase_db


def delete_api_brain_definition(brain_id: UUID) -> None:
    supabase_db = get_supabase_db()

    supabase_db.delete_api_brain_definition(brain_id)
