from enum import Enum
from typing import List, Optional, Union
from uuid import UUID

from auth.auth_bearer import get_current_user
from fastapi import Depends, HTTPException, status
from models.brains import Brain
from models.users import User


class RoleEnum(str, Enum):
    Viewer = "Viewer"
    Editor = "Editor"
    Owner = "Owner"


def has_brain_authorization(
    required_roles: Optional[Union[RoleEnum, List[RoleEnum]]] = RoleEnum.Owner
):
    """
    Decorator to check if the user has the required role(s) for the brain
    param: required_roles: The role(s) required to access the brain
    return: A wrapper function that checks the authorization
    """

    async def wrapper(brain_id: UUID, current_user: User = Depends(get_current_user)):
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

    if required_roles is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing required role",
        )

    brain = Brain(id=brain_id)
    user_brain = brain.get_brain_for_user(user_id)
    if user_brain is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You don't have permission for this brain",
        )

    # Convert single role to a list to handle both cases
    if isinstance(required_roles, str):
        required_roles = [required_roles]

    # Check if the user has at least one of the required roles
    if user_brain.get("rights") not in required_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have the required role(s) for this brain",
        )
