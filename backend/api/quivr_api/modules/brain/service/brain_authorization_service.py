from typing import List, Optional, Union
from uuid import UUID

from fastapi import Depends, HTTPException, status
from quivr_api.middlewares.auth.auth_bearer import get_current_user
from quivr_api.modules.brain.entity.brain_entity import RoleEnum
from quivr_api.modules.brain.service.brain_service import BrainService
from quivr_api.modules.brain.service.brain_user_service import BrainUserService
from quivr_api.modules.user.entity.user_identity import UserIdentity

brain_user_service = BrainUserService()
brain_service = BrainService()


def has_brain_authorization(
    required_roles: Optional[Union[RoleEnum, List[RoleEnum]]] = RoleEnum.Owner
):
    """
    Decorator to check if the user has the required role(s) for the brain
    param: required_roles: The role(s) required to access the brain
    return: A wrapper function that checks the authorization
    """

    async def wrapper(
        brain_id: UUID, current_user: UserIdentity = Depends(get_current_user)
    ):
        nonlocal required_roles
        if isinstance(required_roles, str):
            required_roles = [required_roles]  # Convert single role to a list
        validate_brain_authorization(
            brain_id=brain_id, user_id=current_user.id, required_roles=required_roles
        )

    return wrapper


def validate_brain_authorization(
    brain_id: UUID,
    user_id: UUID,
    required_roles: Optional[Union[RoleEnum, List[RoleEnum]]] = RoleEnum.Owner,
):
    """
    Function to check if the user has the required role(s) for the brain
    param: brain_id: The id of the brain
    param: user_id: The id of the user
    param: required_roles: The role(s) required to access the brain
    return: None
    """

    brain = brain_service.get_brain_details(brain_id, user_id)

    if brain and brain.status == "public":
        return

    if required_roles is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing required role",
        )

    user_brain = brain_user_service.get_brain_for_user(user_id, brain_id)
    if user_brain is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission for this brain",
        )

    # Convert single role to a list to handle both cases
    if isinstance(required_roles, str):
        required_roles = [required_roles]

    # Check if the user has at least one of the required roles
    if user_brain.rights not in required_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have the required role(s) for this brain",
        )
