import time
from datetime import datetime
from secrets import token_hex
from typing import List
from uuid import uuid4

from asyncpg.exceptions import UniqueViolationError
from auth.auth_bearer import AuthBearer, get_current_user
from fastapi import APIRouter, Depends
from logger import get_logger
from models.users import User
from pydantic import BaseModel
from utils.vectors import CommonsDep, fetch_user_id_from_credentials

logger = get_logger(__name__)


class ApiKeyInfo(BaseModel):
    key_id: str
    creation_time: str

class ApiKey(BaseModel):
    api_key: str
    

api_key_router = APIRouter()

@api_key_router.post("/api-key", response_model=ApiKey, dependencies=[Depends(AuthBearer())], tags=["API Key"])
async def create_api_key(commons: CommonsDep, current_user: User = Depends(get_current_user)):
    """
    Create new API key for the current user.

    - `current_user`: The current authenticated user.
    - Returns the newly created API key.

    This endpoint generates a new API key for the current user. The API key is stored in the database and associated with
    the user. It returns the newly created API key.
    """

    date = time.strftime("%Y%m%d")
    user_id = fetch_user_id_from_credentials(commons, date, {"email": current_user.email})

    new_key_id = str(uuid4())
    new_api_key = token_hex(16)
    api_key_inserted = False

    while not api_key_inserted:
        try:
            # Attempt to insert new API key into database
            commons['supabase'].table('api_keys').insert([{
                "key_id": new_key_id,
                "user_id": user_id,
                "api_key": new_api_key,
                "creation_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                "is_active": True
            }]).execute()

            api_key_inserted = True

        except UniqueViolationError:
            # Generate a new API key if the current one is already in use
            new_api_key = token_hex(16)

    logger.info(f"Created new API key for user {current_user.email}.")

    return {"api_key": new_api_key}

@api_key_router.delete("/api-key/{key_id}", dependencies=[Depends(AuthBearer())],  tags=["API Key"])
async def delete_api_key(key_id: str, commons: CommonsDep, current_user: User = Depends(get_current_user)):
    """
    Delete (deactivate) an API key for the current user.

    - `key_id`: The ID of the API key to delete.

    This endpoint deactivates and deletes the specified API key associated with the current user. The API key is marked
    as inactive in the database.

    """

    commons['supabase'].table('api_keys').update({
        "is_active": False,
        "deleted_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }).match({"key_id": key_id, "user_id": current_user.user_id}).execute()

    return {"message": "API key deleted."}

@api_key_router.get("/api-keys", response_model=List[ApiKeyInfo], dependencies=[Depends(AuthBearer())], tags=["API Key"])
async def get_api_keys(commons: CommonsDep, current_user: User = Depends(get_current_user)):
    """
    Get all active API keys for the current user.

    - `current_user`: The current authenticated user.
    - Returns a list of active API keys with their IDs and creation times.

    This endpoint retrieves all the active API keys associated with the current user. It returns a list of API key objects
    containing the key ID and creation time for each API key.
    """

    user_id = fetch_user_id_from_credentials(commons, time.strftime("%Y%m%d"), {"email": current_user.email})

    response = commons['supabase'].table('api_keys').select("key_id, creation_time").filter('user_id', 'eq', user_id).filter('is_active', 'eq', True).execute()
    return response.data