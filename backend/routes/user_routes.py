import time

from auth import AuthBearer, get_current_user
from fastapi import APIRouter, Depends, Request
from models import Brain, UserIdentity, UserUsage
from repository.brain import get_user_default_brain
from repository.user_identity.get_user_identity import get_user_identity
from repository.user_identity.update_user_properties import (
    UserUpdatableProperties,
    update_user_properties,
)

user_router = APIRouter()


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

    userDailyUsage = UserUsage(
        id=current_user.id,
        email=current_user.email,
        openai_api_key=current_user.openai_api_key,
    )
    userSettings = userDailyUsage.get_user_settings()
    max_brain_size = userSettings.get("max_brain_size", 1000000000)

    date = time.strftime("%Y%m%d")
    daily_chat_credit = userSettings.get("daily_chat_credit", 10)

    userDailyUsage = UserUsage(id=current_user.id)
    requests_stats = userDailyUsage.get_user_usage()
    default_brain = get_user_default_brain(current_user.id)

    if default_brain:
        defaul_brain_size = Brain(id=default_brain.brain_id).brain_size
    else:
        defaul_brain_size = 0

    return {
        "email": current_user.email,
        "max_brain_size": max_brain_size,
        "current_brain_size": defaul_brain_size,
        "daily_chat_credit": daily_chat_credit,
        "requests_stats": requests_stats,
        "models": userSettings.get("models", []),
        "date": date,
        "id": current_user.id,
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
    return update_user_properties(current_user.id, user_identity_updatable_properties)


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
    return get_user_identity(current_user.id)
