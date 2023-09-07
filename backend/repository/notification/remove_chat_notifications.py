from uuid import UUID
from models.settings import get_supabase_db


def remove_chat_notifications(chat_id: UUID) -> None:
    """
    Remove all notifications for a chat
    """
    supabase_db = get_supabase_db()

    supabase_db.remove_notifications_by_chat_id(chat_id)
