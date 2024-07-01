from typing import Annotated

from fastapi import APIRouter, Depends

from quivr_core.api.modules.brain.service.brain_user_service import BrainUserService
from quivr_core.api.modules.dependencies import get_current_user, get_service
from quivr_core.api.modules.user.dto.inputs import UserUpdatableProperties
from quivr_core.api.modules.user.entity.user_identity import UserIdentity
from quivr_core.api.modules.user.service.user_service import UserService

user_router = APIRouter()
brain_user_service = BrainUserService()

UserServiceDep = Annotated[UserService, Depends(get_service(UserService))]

UserIdentityDep = Annotated[UserIdentity, Depends(get_current_user)]


@user_router.get("/user", tags=["User"])
async def get_user_endpoint(
    current_user: UserIdentityDep, user_service: UserServiceDep
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

    user_settings = user_service.get_user_settings(current_user.id)

    return {
        "email": current_user.email,
        "current_brain_size": 0,
        "models": user_settings.get("models", []),
        "id": current_user.id,
    }


@user_router.put(
    "/user/identity",
    tags=["User"],
)
def update_user_identity_route(
    user_identity_updatable_properties: UserUpdatableProperties,
    current_user: UserIdentityDep,
    user_service: UserServiceDep,
) -> UserIdentity:
    """
    Update user identity.
    """
    return user_service.update_user_properties(
        current_user.id, user_identity_updatable_properties
    )


@user_router.get(
    "/user/identity",
    tags=["User"],
)
def get_user_identity_route(
    current_user: UserIdentityDep,
    user_service: UserServiceDep,
) -> UserIdentity:
    """
    Get user identity.
    """
    return user_service.get_user_identity(current_user.id)


@user_router.delete(
    "/user_data",
    tags=["User"],
)
async def delete_user_data_route(
    current_user: UserIdentityDep,
    user_service: UserServiceDep,
):
    """
    Delete a user.
    - `user_id`: The ID of the user to delete.

    This endpoint deletes a user from the system.
    """

    user_service.delete_user_data(current_user.id)

    return {"message": "User deleted successfully"}
