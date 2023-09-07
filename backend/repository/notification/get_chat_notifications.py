from typing import List
from uuid import UUID

from models.notifications import Notification
from models.settings import get_supabase_db


def get_chat_notifications(chat_id: UUID) -> List[Notification]:
    """
    Get notifications by chat_id
    """
    supabase_db = get_supabase_db()

    return supabase_db.get_notifications_by_chat_id(chat_id)
