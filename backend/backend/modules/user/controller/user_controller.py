from fastapi import APIRouter, Depends, Request

from backend.middlewares.auth import AuthBearer, get_current_user
from backend.modules.brain.service.brain_user_service import BrainUserService
from backend.modules.user.dto.inputs import UserUpdatableProperties
from backend.modules.user.entity.user_identity import UserIdentity
from backend.modules.user.repository.users import Users
from backend.modules.user.service.user_usage import UserUsage

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

    monthly_chat_credit = user_settings.get("monthly_chat_credit", 10)

    user_daily_usage = UserUsage(id=current_user.id)

    return {
        "email": current_user.email,
        "max_brain_size": max_brain_size,
        "current_brain_size": 0,
        "monthly_chat_credit": monthly_chat_credit,
        "models": user_settings.get("models", []),
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


@user_router.delete(
    "/user_data",
    dependencies=[Depends(AuthBearer())],
    tags=["User"],
)
async def delete_user_data_route(
    current_user: UserIdentity = Depends(get_current_user),
):
    """
    Delete a user.

    - `user_id`: The ID of the user to delete.

    This endpoint deletes a user from the system.
    """

    user_repository.delete_user_data(current_user.id)

    return {"message": "User deleted successfully"}


@user_router.get(
    "/user/credits",
    dependencies=[Depends(AuthBearer())],
    tags=["User"],
)
def get_user_credits(
    current_user: UserIdentity = Depends(get_current_user),
) -> int:
    """
    Get user remaining credits.
    """
    return user_repository.get_user_credits(current_user.id)
