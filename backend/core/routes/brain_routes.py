from uuid import UUID

from auth import AuthBearer, get_current_user
from fastapi import APIRouter, Depends, HTTPException
from logger import get_logger
from models.brains import (
    Brain,
    get_default_user_brain,
    get_default_user_brain_or_create_new,
)
from models.settings import BrainRateLimiting
from models.users import User

from routes.authorizations.brain_authorization import RoleEnum, has_brain_authorization

logger = get_logger(__name__)

brain_router = APIRouter()


# get all brains
@brain_router.get("/brains/", dependencies=[Depends(AuthBearer())], tags=["Brain"])
async def brain_endpoint(current_user: User = Depends(get_current_user)):
    """
    Retrieve all brains for the current user.

    - `current_user`: The current authenticated user.
    - Returns a list of all brains registered for the user.

    This endpoint retrieves all the brains associated with the current authenticated user. It returns a list of brains objects
    containing the brain ID and brain name for each brain.
    """
    brain = Brain()
    brains = brain.get_user_brains(current_user.id)
    return {"brains": brains}


# get default brain
@brain_router.get(
    "/brains/default/", dependencies=[Depends(AuthBearer())], tags=["Brain"]
)
async def get_default_brain_endpoint(current_user: User = Depends(get_current_user)):
    """
    Retrieve the default brain for the current user. If the user doesnt have one, it creates one.

    - `current_user`: The current authenticated user.
    - Returns the default brain for the user.

    This endpoint retrieves the default brain associated with the current authenticated user.
    The default brain is defined as the brain marked as default in the brains_users table.
    """

    brain = get_default_user_brain_or_create_new(current_user)
    return {"id": brain.id, "name": brain.name, "rights": "Owner"}


# get one brain - Currently not used in FE
@brain_router.get(
    "/brains/{brain_id}/",
    dependencies=[Depends(AuthBearer()), Depends(has_brain_authorization())],
    tags=["Brain"],
)
async def get_brain_endpoint(
    brain_id: UUID,
):
    """
    Retrieve details of a specific brain by brain ID.

    - `brain_id`: The ID of the brain to retrieve details for.
    - Returns the brain ID and its history.

    This endpoint retrieves the details of a specific brain identified by the provided brain ID. It returns the brain ID and its
    history, which includes the brain messages exchanged in the brain.
    """
    brain = Brain(id=brain_id)
    brains = brain.get_brain_details()
    if len(brains) > 0:
        return brains[0]
    else:
        return HTTPException(
            status_code=404,
            detail="Brain not found",
        )


# create new brain
@brain_router.post("/brains/", dependencies=[Depends(AuthBearer())], tags=["Brain"])
async def create_brain_endpoint(
    brain: Brain,
    current_user: User = Depends(get_current_user),
):
    """
    Create a new brain with given
        name
        status
        model
        max_tokens
        temperature
    In the brains table & in the brains_users table and put the creator user as 'Owner'
    """

    user_brains = brain.get_user_brains(current_user.id)
    max_brain_per_user = BrainRateLimiting().max_brain_per_user

    if len(user_brains) >= max_brain_per_user:
        raise HTTPException(
            status_code=429,
            detail=f"Maximum number of brains reached ({max_brain_per_user}).",
        )

    brain.create_brain()  # pyright: ignore reportPrivateUsage=none
    default_brain = get_default_user_brain(current_user)
    if default_brain:
        logger.info(f"Default brain already exists for user {current_user.id}")
        brain.create_brain_user(  # pyright: ignore reportPrivateUsage=none
            user_id=current_user.id, rights="Owner", default_brain=False
        )
    else:
        logger.info(
            f"Default brain does not exist for user {current_user.id}. It will be created."
        )
        brain.create_brain_user(  # pyright: ignore reportPrivateUsage=none
            user_id=current_user.id, rights="Owner", default_brain=True
        )

    return {
        "id": brain.id,  # pyright: ignore reportPrivateUsage=none
        "name": brain.name,
        "rights": "Owner",
    }


# update existing brain
@brain_router.put(
    "/brains/{brain_id}/",
    dependencies=[
        Depends(
            AuthBearer(),
        ),
        Depends(has_brain_authorization([RoleEnum.Editor, RoleEnum.Owner])),
    ],
    tags=["Brain"],
)
async def update_brain_endpoint(
    brain_id: UUID,
    input_brain: Brain,
):
    """
    Update an existing brain with new brain configuration
    """
    input_brain.id = brain_id
    print("brain", input_brain)

    input_brain.update_brain_fields()
    return {"message": f"Brain {brain_id} has been updated."}


# set as default brain
@brain_router.post(
    "/brains/{brain_id}/default",
    dependencies=[
        Depends(
            AuthBearer(),
        ),
        Depends(has_brain_authorization()),
    ],
    tags=["Brain"],
)
async def set_as_default_brain_endpoint(
    brain_id: UUID,
    user: User = Depends(get_current_user),
):
    """
    Set a brain as default for the current user.
    """
    brain = Brain(id=brain_id)

    brain.set_as_default_brain_for_user(user)

    return {"message": f"Brain {brain_id} has been set as default brain."}
