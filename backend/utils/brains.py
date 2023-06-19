from uuid import UUID

from fastapi import APIRouter
from logger import get_logger
from models.brains import Brain, BrainToUpdate
from models.users import User
from models.settings import CommonsDep
from utils.users import fetch_user_id_from_credentials

logger = get_logger(__name__)

brain_router = APIRouter()

def get_user_brains(commons: CommonsDep, user_id):
    response = commons['supabase'].from_('brains_users') \
    .select('id:brain_id, brains (id: brain_id, name)') \
    .filter('user_id', 'eq', user_id) \
   .execute()
    
    return [item['brains'] for item in response.data]

def get_brain(commons: CommonsDep, brain_id):
    response = commons['supabase'].from_('brains').select('brainId:brain_id, brainName:brain_name').filter("brain_id", "eq", brain_id).execute()
    return response.data

def get_brain_details(commons: CommonsDep, brain_id):
    response = commons['supabase'].from_('brains').select('id:brain_id, name, *').filter("brain_id", "eq", brain_id).execute()
    return response.data

def delete_brain(commons: CommonsDep, brain_id):
    # Does it also delete it in brains_users and brains_vectors ? 
    commons['supabase'].table("brains").delete().match({"brain_id": brain_id}).execute()

def create_brain(commons: CommonsDep, brain = Brain):
   response = commons['supabase'].table("brains").insert(
        {"name": brain.name}).execute() 
   return response.data

def create_brain_user(commons: CommonsDep, brain_id, user_id, rights):
   response = commons['supabase'].table("brains_users").insert(
        { "brain_id": brain_id, "user_id": user_id, "rights": rights}).execute() 
   return response.data

def create_brain_vector(commons: CommonsDep, brain_id, vector_id):
   response = commons['supabase'].table("brains_users").insert(
        { "brain_id": brain_id, "vector_id": vector_id}).execute() 
   return response.data

def get_vector_ids_from_file_sha1(commons: CommonsDep, file_sha1: str):
    vectorsResponse = commons['supabase'].table("vectors").select("id").filter("metadata->>file_sha1", "eq", file_sha1) \
        .execute()
    print('vectorsResponse', vectorsResponse.data)
    return vectorsResponse.data

def update_brain_fields(commons: CommonsDep,  brain: BrainToUpdate):
    # Need to only get the not undefined brain fields passed Optional['Brain'] -> create a BrainToUpdate type 
    commons['supabase'].table("brains").update(
        { "name": brain.name}).match({"brain_id": brain.brain_id}).execute()
    logger.info(f"Brain {brain.brain_id} updated")

def update_brain_with_file(commons: CommonsDep,brain_id:UUID , file_sha1: str ):
        # add all the vector Ids to the brains_vectors  with the given brain.brain_id
        vector_ids = get_vector_ids_from_file_sha1(commons, file_sha1)
        for vector_id in vector_ids: 
            create_brain_vector(commons, brain_id=brain_id, vector_id = vector_id)
