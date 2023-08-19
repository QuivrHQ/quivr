from uuid import UUID

from auth import AuthBearer, get_current_user
from fastapi import APIRouter, Depends, HTTPException
from logger import get_logger
from models.databases.supabase.brains import (
    BrainUpdatableProperties,
    CreateBrainProperties,
)
from models.settings import BrainRateLimiting
from models.users import User
from repository.brain.create_brain import create_brain
from repository.brain.create_brain_user import create_brain_user
from repository.brain.get_brain_details import get_brain_details
from repository.brain.get_default_user_brain import get_user_default_brain
from repository.brain.get_default_user_brain_or_create_new import (
    get_default_user_brain_or_create_new,
)
from repository.brain.get_user_brains import get_user_brains
from repository.brain.set_as_default_brain_for_user import (
    set_as_default_brain_for_user,
)
from repository.brain.update_brain import update_brain_by_id
from repository.prompt.delete_prompt_py_id import delete_prompt_by_id
from repository.prompt.get_prompt_by_id import get_prompt_by_id

from routes.authorizations.brain_authorization import (
    has_brain_authorization,
)
from routes.authorizations.types import RoleEnum

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
    brains = get_user_brains(current_user.id)
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
    return {"id": brain.brain_id, "name": brain.name, "rights": "Owner"}


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

    brain_details = get_brain_details(brain_id)
    if brain_details is None:
        raise HTTPException(
            status_code=404,
            detail="Brain details not found",
        )

    return brain_details


# create new brain
@brain_router.post("/brains/", dependencies=[Depends(AuthBearer())], tags=["Brain"])
async def create_brain_endpoint(
    brain: CreateBrainProperties,
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

    user_brains = get_user_brains(current_user.id)
    max_brain_per_user = BrainRateLimiting().max_brain_per_user

    if len(user_brains) >= max_brain_per_user:
        raise HTTPException(
            status_code=429,
            detail=f"Maximum number of brains reached ({max_brain_per_user}).",
        )

    new_brain = create_brain(
        brain,
    )
    default_brain = get_user_default_brain(current_user.id)
    if default_brain:
        logger.info(f"Default brain already exists for user {current_user.id}")
        create_brain_user(
            user_id=current_user.id,
            brain_id=new_brain.brain_id,
            rights=RoleEnum.Owner,
            is_default_brain=False,
        )
    else:
        logger.info(
            f"Default brain does not exist for user {current_user.id}. It will be created."
        )
        create_brain_user(
            user_id=current_user.id,
            brain_id=new_brain.brain_id,
            rights=RoleEnum.Owner,
            is_default_brain=True,
        )

    return {
        "id": new_brain.brain_id,
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
    input_brain: BrainUpdatableProperties,
):
    """
    Update an existing brain with new brain configuration
    """

    # Remove prompt if it is private and no longer used by brain
    if input_brain.prompt_id is None:
        existing_brain = get_brain_details(brain_id)
        if existing_brain is None:
            raise HTTPException(
                status_code=404,
                detail="Brain not found",
            )
        prompt_id = existing_brain.prompt_id
        if prompt_id is not None:
            prompt = get_prompt_by_id(prompt_id)
            if prompt is not None and prompt.status == "private":
                delete_prompt_by_id(prompt_id)

    update_brain_by_id(brain_id, input_brain)

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

    set_as_default_brain_for_user(user.id, brain_id)

    return {"message": f"Brain {brain_id} has been set as default brain."}
