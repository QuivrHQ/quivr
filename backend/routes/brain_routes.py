import os
import time
from typing import Optional
from uuid import UUID

from auth.auth_bearer import AuthBearer, get_current_user
from fastapi import APIRouter, Depends, Request
from logger import get_logger
from models.brains import Brain, BrainToUpdate
from models.settings import CommonsDep, common_dependencies
from models.users import User
from utils.users import fetch_user_id_from_credentials

logger = get_logger(__name__)

brain_router = APIRouter()

def get_user_brains(commons, user_id):
    response = commons['supabase'].from_('brains_users') \
        .select('brain_id', {'brainName': 'brains.name'}) \
        .join('brains:brain_id=brains_users.brain_id') \
        .filter('brains_users.user_id', 'eq', user_id) \
        .execute()

    return response.data

def get_brain(commons, brain_id):
    response = commons['supabase'].from_('brains').select('brainId:brain_id, brainName:brain_name').filter("brain_id", "eq", brain_id).execute()
    return response.data

def get_brain_details(commons, brain_id):
    response = commons['supabase'].from_('brains').select('*').filter("brain_id", "eq", brain_id).execute()
    return response.data

def delete_brain(commons, brain_id):
    # Does it also delete it in brains_users and brains_vectors ? 
    commons['supabase'].table("brains").delete().match({"brain_id": brain_id}).execute()

def create_brain(commons, brain = Brain):
   response = commons['supabase'].table("brains").insert(
        brain).execute() 
   return response.data

def create_brain_user(commons, brain_id, user_id, rights):
   response = commons['supabase'].table("brains_users").insert(
        { "brain_id": brain_id, "user_id": user_id, "rights": rights}).execute() 
   return response.data

def create_brain_vector(commons, brain_id, vector_id):
   response = commons['supabase'].table("brains_users").insert(
        { "brain_id": brain_id, "vector_id": vector_id}).execute() 
   return response.data

def get_vector_ids_from_file_sha1(commons, file_sha1: str):
    vectorsResponse = commons['supabase'].table("vectors").select("id").filter("metadata->>file_sha1", "eq", file_sha1) \
        .execute()
    print('vectorsResponse', vectorsResponse.data)
    return vectorsResponse.data

def update_brain_fields(commons,  brain: BrainToUpdate):
    # Need to only get the not undefined brain fields passed Optional['Brain'] -> create a BrainToUpdate type 
    commons['supabase'].table("brains").update(
        { "brain_name": brain.brain_name}).match({"brain_id": brain.brain_id}).execute()
    logger.info(f"Brain {brain.brain_id} updated")

def update_brain_with_file(commons,brain_id:UUID , file_sha1: str ):
        # add all the vector Ids to the brains_vectors  with the given brain.brain_id
        vector_ids = get_vector_ids_from_file_sha1(commons, file_sha1)
        for vector_id in vector_ids: 
            create_brain_vector(commons, brain_id=brain_id, vector_id = vector_id)

# get all brains
@brain_router.get("/brain", dependencies=[Depends(AuthBearer())], tags=["Brain"])
async def brain_endpoint( current_user: User = Depends(get_current_user)):
    """
    Retrieve all brains for the current user.

    - `current_user`: The current authenticated user.
    - Returns a list of all brains registered for the user.

    This endpoint retrieves all the brains associated with the current authenticated user. It returns a list of brains objects
    containing the brain ID and brain name for each brain.
    """
    commons = common_dependencies()
    user_id = fetch_user_id_from_credentials(commons,  {"email": current_user.email})
    brains = get_user_brains(commons, user_id)
    return {"brains": brains}

# get one brain
@brain_router.get("/brain/{brain_id}", dependencies=[Depends(AuthBearer())], tags=["Brain"])
async def brain_endpoint( brain_id: UUID):
    """
    Retrieve details of a specific brain by brain ID.

    - `brain_id`: The ID of the brain to retrieve details for.
    - Returns the brain ID and its history.

    This endpoint retrieves the details of a specific brain identified by the provided brain ID. It returns the brain ID and its
    history, which includes the brain messages exchanged in the brain.
    """
    commons = common_dependencies()
    brains = get_brain_details(commons, brain_id)
    if len(brains) > 0:
        return {"brainId": brain_id, "brainName": brains[0]['brain_name'], "status": brains[0]['status']}
    else:
        return {"error": f'No brain found with brain_id {brain_id}'}

# delete one brain
@brain_router.delete("/brain/{brain_id}", dependencies=[Depends(AuthBearer())], tags=["Brain"])
async def brain_endpoint( brain_id: UUID):
    """
    Delete a specific brain by brain ID.
    """
    commons = common_dependencies()
    delete_brain(commons, brain_id)
    return {"message": f"{brain_id}  has been deleted."}


# create new brain
@brain_router.post("/brain", dependencies=[Depends(AuthBearer())], tags=["Brain"])
async def brain_endpoint(request: Request, brain: Brain, current_user: User = Depends(get_current_user)):
    """
    Create a new brain with given 
        brain_name
        status
        model
        max_tokens
        temperature
    In the brains table & in the brains_users table and put the creator user as 'Owner'
    """
    commons = common_dependencies() 
    user_id = fetch_user_id_from_credentials(commons,  {"email": current_user.email})
    created_brain = create_brain(commons, brain)
    # create a brain 
    create_brain_user(created_brain['brain_id'], user_id, rights='Owner')

    return {"brainId": created_brain['brain_id'], "brainName": created_brain['brain_name']}

# update existing brain
@brain_router.put("/brain/{brain_id}", dependencies=[Depends(AuthBearer())], tags=["Brain"])
async def brain_endpoint(request: Request, brain_id: UUID, brain: BrainToUpdate, fileName: Optional[str], current_user: User = Depends(get_current_user)):
    """
    Update an existing brain with new brain parameters/files.
    If the file is contained in Add file to brain : 
        if given a fileName/ file sha1 / -> add all the vector Ids to the brains_vectors 
    Modify other brain fields: 
        name, status, model, max_tokens, temperature 
    Return modified brain ? No need -> do an optimistic update 
    """
    commons = common_dependencies()
    # Add new file to brain , il file_sha1 already exists in brains_vectors -> out (not now)
    if brain.file_sha1 : 
        # add all the vector Ids to the brains_vectors  with the given brain.brain_id
        update_brain_with_file(commons, brain_id= brain.brain_id, file_sha1=brain.brain_name)
        print("brain:", brain)

    update_brain_fields(commons, brain)
    return {"message": f"Brain {brain_id} has been updated."}

