from functools import wraps
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from models.brains import Brain
from models.users import User


def has_brain_authorization(required_role: Optional[str] = "Owner"):
    def decorator(func):
        @wraps(func)
        async def wrapper(current_user: User, *args, **kwargs):
            brain_id: Optional[UUID] = kwargs.get("brain_id")
            user_id = current_user.id

            if brain_id is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Missing brain ID",
                )

            validate_brain_authorization(
                brain_id, user_id=user_id, required_role=required_role
            )

            return await func(*args, **kwargs)

        return wrapper

    return decorator


def validate_brain_authorization(
    brain_id: UUID,
    user_id: UUID,
    required_role: Optional[str] = "Owner",
):
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
