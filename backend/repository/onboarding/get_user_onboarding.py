from uuid import UUID

from models.databases.supabase.onboarding import OnboardingStates
from models.settings import get_supabase_db


def get_user_onboarding(user_id: UUID) -> OnboardingStates | None:
    """
    Get a user's onboarding status

    Args:
        user_id (UUID): The id of the user

    Returns:
        Onboardings: The user's onboarding status
    """
    supabase_db = get_supabase_db()
    return supabase_db.get_user_onboarding(user_id)
