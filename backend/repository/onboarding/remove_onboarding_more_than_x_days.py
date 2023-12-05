from models.settings import get_supabase_db


def remove_onboarding_more_than_x_days(days: int):
    """
    Remove onboarding if it is older than x days
    """
    supabase_db = get_supabase_db()

    supabase_db.remove_onboarding_more_than_x_days(days)
