import os
import time
from typing import Optional
from uuid import UUID

from auth.auth_bearer import AuthBearer, get_current_user
from fastapi import APIRouter, Depends, Request
from logger import get_logger
from models.brains import Brain
from models.settings import CommonsDep, common_dependencies
from models.users import User
from pydantic import BaseModel
from utils.users import fetch_user_id_from_credentials

logger = get_logger(__name__)

brain_router = APIRouter()


class BrainToUpdate(BaseModel):
    brain_id: UUID
    name: Optional[str] = "New Brain"
    status: Optional[str] = "public"
    model: Optional[str] = "gpt-3.5-turbo-0613"
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = 256
    file_sha1: Optional[str] = ""


# get all brains
@brain_router.get("/brains", dependencies=[Depends(AuthBearer())], tags=["Brain"])
async def brain_endpoint(current_user: User = Depends(get_current_user)):
    """
    Retrieve all brains for the current user.

    - `current_user`: The current authenticated user.
    - Returns a list of all brains registered for the user.

    This endpoint retrieves all the brains associated with the current authenticated user. It returns a list of brains objects
    containing the brain ID and brain name for each brain.
    """
    commons = common_dependencies()
    brain = Brain()
    user_id = fetch_user_id_from_credentials(commons, {"email": current_user.email})
    brains = brain.get_user_brains(user_id)
    return {"brains": brains}


# get one brain
@brain_router.get(
    "/brains/{brain_id}", dependencies=[Depends(AuthBearer())], tags=["Brain"]
)
async def brain_endpoint(brain_id: UUID):
    """
    Retrieve details of a specific brain by brain ID.

    - `brain_id`: The ID of the brain to retrieve details for.
    - Returns the brain ID and its history.

    This endpoint retrieves the details of a specific brain identified by the provided brain ID. It returns the brain ID and its
    history, which includes the brain messages exchanged in the brain.
    """
    brain = Brain(brain_id=brain_id)
    brains = brain.get_brain_details()
    if len(brains) > 0:
        return {
            "brainId": brain_id,
            "brainName": brains[0]["name"],
            "status": brains[0]["status"],
        }
    else:
        return {"error": f"No brain found with brain_id {brain_id}"}


# delete one brain
@brain_router.delete(
    "/brains/{brain_id}", dependencies=[Depends(AuthBearer())], tags=["Brain"]
)
async def brain_endpoint(brain_id: UUID):
    """
    Delete a specific brain by brain ID.
    """
    brain = Brain(brain_id=brain_id)
    brain.delete_brain()
    return {"message": f"{brain_id}  has been deleted."}


class BrainObject(BaseModel):
    brain_id: Optional[UUID]
    name: Optional[str] = "New Brain"
    status: Optional[str] = "public"
    model: Optional[str] = "gpt-3.5-turbo-0613"
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = 256
    file_sha1: Optional[str] = ""


# create new brain
@brain_router.post("/brains", dependencies=[Depends(AuthBearer())], tags=["Brain"])
async def brain_endpoint(
    request: Request,
    brain: BrainObject,
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
    commons = common_dependencies()
    brain = Brain(name=brain.name)
    user_id = fetch_user_id_from_credentials(commons, {"email": current_user.email})
    created_brain = brain.create_brain(brain.name)[0]
    # create a brain X user entry
    brain.create_brain_user(created_brain["brain_id"], user_id, rights="Owner")

    return {"id": created_brain["brain_id"], "name": created_brain["name"]}


# update existing brain
@brain_router.put(
    "/brains/{brain_id}", dependencies=[Depends(AuthBearer())], tags=["Brain"]
)
async def brain_endpoint(
    request: Request,
    brain_id: UUID,
    input_brain: Brain,
    fileName: Optional[str],
    current_user: User = Depends(get_current_user),
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
    brain = Brain(brain_id=brain_id)

    # Add new file to brain , il file_sha1 already exists in brains_vectors -> out (not now)
    if brain.file_sha1:
        # add all the vector Ids to the brains_vectors  with the given brain.brain_id
        brain.update_brain_with_file(file_sha1=input_brain.file_sha1)
        print("brain:", brain)

    brain.update_brain_fields(commons, brain)
    return {"message": f"Brain {brain_id} has been updated."}
