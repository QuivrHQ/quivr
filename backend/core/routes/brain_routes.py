from uuid import UUID

from auth import AuthBearer, get_current_user
from fastapi import APIRouter, Depends, HTTPException
from logger import get_logger
from models.brains import (Brain, get_default_user_brain,
                           get_default_user_brain_or_create_new)
from models.settings import common_dependencies
from models.users import User
from routes.authorizations.brain_authorization import has_brain_authorization

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
    return {
        "id": brain.id,
        "name": brain.name,
    }


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
        return {
            "id": brain_id,
            "name": brains[0]["name"],
            "status": brains[0]["status"],
        }
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

    brain = Brain(name=brain.name)  # pyright: ignore reportPrivateUsage=none

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
    }


# update existing brain
@brain_router.put(
    "/brains/{brain_id}/",
    dependencies=[
        Depends(
            AuthBearer(),
        ),
        Depends(has_brain_authorization()),
    ],
    tags=["Brain"],
)
async def update_brain_endpoint(
    brain_id: UUID,
    input_brain: Brain,
):
    """
    Update an existing brain with new brain parameters/files.
    If the file is contained in Add file to brain :
        if given a fileName/ file sha1 / -> add all the vector Ids to the brains_vectors
    Modify other brain fields:
        name, status, model, max_tokens, temperature
    Return modified brain ? No need -> do an optimistic update
    """
    commons = common_dependencies()
    brain = Brain(id=brain_id)

    # Add new file to brain , il file_sha1 already exists in brains_vectors -> out (not now)
    if brain.file_sha1:  # pyright: ignore reportPrivateUsage=none
        # add all the vector Ids to the brains_vectors  with the given brain.brain_id
        brain.update_brain_with_file(
            file_sha1=input_brain.file_sha1  # pyright: ignore reportPrivateUsage=none
        )

    brain.update_brain_fields(commons, brain)  # pyright: ignore reportPrivateUsage=none
    return {"message": f"Brain {brain_id} has been updated."}
