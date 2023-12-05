from uuid import UUID

from models.databases.supabase.onboarding import (
    OnboardingStates,
)
from models.settings import get_supabase_db


def create_user_onboarding(user_id: UUID) -> OnboardingStates:
    """Update user onboarding information by user_id"""

    supabase_db = get_supabase_db()
    created_user_onboarding = supabase_db.create_user_onboarding(user_id)

    return created_user_onboarding
