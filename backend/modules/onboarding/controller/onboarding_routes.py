from fastapi import APIRouter, Depends
from middlewares.auth import (  # Assuming you have a get_current_user function
    AuthBearer,
    get_current_user,
)
from modules.onboarding.dto.inputs import OnboardingUpdatableProperties
from modules.onboarding.entity.onboarding import OnboardingStates
from modules.onboarding.service.onboarding_service import OnboardingService
from modules.user.entity.user_identity import UserIdentity

onboarding_router = APIRouter()

onboardingService = OnboardingService()


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

    return onboardingService.get_user_onboarding(current_user.id)


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

    return onboardingService.update_user_onboarding(current_user.id, onboarding)
