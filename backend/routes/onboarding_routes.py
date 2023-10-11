from auth import (
    AuthBearer,
    get_current_user,  # Assuming you have a get_current_user function
)
from fastapi import APIRouter, Depends
from models.databases.supabase.onboarding import (
    OnboardingStates,
    OnboardingUpdatableProperties,
)
from models.user_identity import UserIdentity
from repository.onboarding.get_user_onboarding import get_user_onboarding
from repository.onboarding.update_user_onboarding import update_user_onboarding

onboarding_router = APIRouter()


@onboarding_router.get(
    "/onboarding",
    dependencies=[Depends(AuthBearer())],
    tags=["Onboarding"],
)
async def get_user_onboarding_handler(
    current_user: UserIdentity = Depends(get_current_user),
) -> OnboardingStates | None:
    """
    Get user onboarding information for the current user
    """

    return get_user_onboarding(current_user.id)


@onboarding_router.put(
    "/onboarding",
    dependencies=[Depends(AuthBearer())],
    tags=["Onboarding"],
)
async def update_user_onboarding_handler(
    onboarding: OnboardingUpdatableProperties,
    current_user: UserIdentity = Depends(get_current_user),
) -> OnboardingStates:
    """
    Update user onboarding information for the current user
    """

    return update_user_onboarding(current_user.id, onboarding)
