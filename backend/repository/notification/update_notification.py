from models.databases.supabase.notifications import NotificationUpdatableProperties
from models.settings import get_supabase_db


def update_notification_by_id(
    notification_id, notification: NotificationUpdatableProperties
):
    """
    Update a notification
    """
    supabase_db = get_supabase_db()

    return supabase_db.update_notification_by_id(notification_id, notification)
