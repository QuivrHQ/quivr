import time

from fastapi import APIRouter, Depends, Request
from middlewares.auth import AuthBearer, get_current_user
from models import UserUsage
from modules.brain.service.brain_user_service import BrainUserService
from modules.brain.service.brain_vector_service import BrainVectorService
from modules.user.dto.inputs import UserUpdatableProperties
from modules.user.entity.user_identity import UserIdentity
from modules.user.repository.users import Users

user_router = APIRouter()
brain_user_service = BrainUserService()
user_repository = Users()


@user_router.get("/user", dependencies=[Depends(AuthBearer())], tags=["User"])
async def get_user_endpoint(
    request: Request, current_user: UserIdentity = Depends(get_current_user)
):
    """
    Get user information and statistics.

    - `current_user`: The current authenticated user.
    - Returns the user's email, maximum brain size, current brain size, maximum requests number, requests statistics, and the current date.

    This endpoint retrieves information and statistics about the authenticated user. It includes the user's email, maximum brain size,
    current brain size, maximum requests number, requests statistics, and the current date. The brain size is calculated based on the
    user's uploaded vectors, and the maximum brain size is obtained from the environment variables. The requests statistics provide
    information about the user's API usage.
    """

    user_daily_usage = UserUsage(
        id=current_user.id,
        email=current_user.email,
    )
    user_settings = user_daily_usage.get_user_settings()
    max_brain_size = user_settings.get("max_brain_size", 1000000000)

    date = time.strftime("%Y%m%d")
    monthly_chat_credit = user_settings.get("monthly_chat_credit", 10)

    user_daily_usage = UserUsage(id=current_user.id)
    requests_stats = user_daily_usage.get_user_usage()
    default_brain = brain_user_service.get_user_default_brain(current_user.id)

    if default_brain:
        defaul_brain_size = BrainVectorService(default_brain.brain_id).brain_size
    else:
        defaul_brain_size = 0

    return {
        "email": current_user.email,
        "max_brain_size": max_brain_size,
        "current_brain_size": defaul_brain_size,
        "monthly_chat_credit": monthly_chat_credit,
        "requests_stats": requests_stats,
        "models": user_settings.get("models", []),
        "date": date,
        "id": current_user.id,
        "is_premium": user_settings["is_premium"],
    }


@user_router.put(
    "/user/identity",
    dependencies=[Depends(AuthBearer())],
    tags=["User"],
)
def update_user_identity_route(
    user_identity_updatable_properties: UserUpdatableProperties,
    current_user: UserIdentity = Depends(get_current_user),
) -> UserIdentity:
    """
    Update user identity.
    """
    return user_repository.update_user_properties(
        current_user.id, user_identity_updatable_properties
    )


@user_router.get(
    "/user/identity",
    dependencies=[Depends(AuthBearer())],
    tags=["User"],
)
def get_user_identity_route(
    current_user: UserIdentity = Depends(get_current_user),
) -> UserIdentity:
    """
    Get user identity.
    """
    return user_repository.get_user_identity(current_user.id)
