from fastapi import APIRouter, Depends
from quivr_api.middlewares.auth import AuthBearer, get_current_user
from quivr_api.modules.user.entity.user_identity import UserIdentity

onboarding_router = APIRouter()


@onboarding_router.get(
    "/onboarding",
    dependencies=[Depends(AuthBearer())],
    tags=["Deprecated"],
)
async def get_user_onboarding_handler(
    current_user: UserIdentity = Depends(get_current_user),
) -> dict:
    """
    Get user onboarding information for the current user
    """

    return {"status": "Deprecated and will be removed in v0.1"}
