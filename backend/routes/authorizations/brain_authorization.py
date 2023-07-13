from typing import Optional
from uuid import UUID

from auth.auth_bearer import get_current_user
from fastapi import Depends, HTTPException, status
from models.brains import Brain
from models.users import User


def has_brain_authorization(required_role: Optional[str] = "Owner"):
    """
    Decorator to check if the user has the required role for the brain
    param: required_role: The role required to access the brain
    return: A wrapper function that checks the authorization
    """

    async def wrapper(brain_id: UUID, current_user: User = Depends(get_current_user)):
        validate_brain_authorization(
            brain_id=brain_id, user_id=current_user.id, required_role=required_role
        )

    return wrapper


def validate_brain_authorization(
    brain_id: UUID,
    user_id: UUID,
    required_role: Optional[str] = "Owner",
):
    """
    Function to check if the user has the required role for the brain
    param: brain_id: The id of the brain
    param: user_id: The id of the user
    param: required_role: The role required to access the brain
    return: None
    """

    if required_role is None:
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

    # TODO: Update this logic when we have more roles
    # Eg: Owner > Admin > User ... this should be taken into account
    if user_brain.get("rights") != required_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have the required role for this brain",
        )
