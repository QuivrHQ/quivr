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

    Example:
    ```
    POST /api-key

    Response:
    {
        "api_key": "a8a62be1b5a2e46b1d6a"
    }
    ```
    """

@api_key_router.delete("/api-key/{key_id}", dependencies=[Depends(AuthBearer())],  tags=["API Key"])
async def delete_api_key(key_id: str, commons: CommonsDep, current_user: User = Depends(get_current_user)):
    """
    Delete (deactivate) an API key for the current user.

    - `key_id`: The ID of the API key to delete.

    This endpoint deactivates and deletes the specified API key associated with the current user. The API key is marked
    as inactive in the database.

    Example:
    ```
    DELETE /api-key/a8a62be1b5a2e46b1d6a

    Response:
    {
        "message": "API key deleted."
    }
    ```
    """

@api_key_router.get("/api-keys", response_model=List[ApiKeyInfo], dependencies=[Depends(AuthBearer())], tags=["API Key"])
async def get_api_keys(commons: CommonsDep, current_user: User = Depends(get_current_user)):
    """
    Get all active API keys for the current user.

    - `current_user`: The current authenticated user.
    - Returns a list of active API keys with their IDs and creation times.

    This endpoint retrieves all the active API keys associated with the current user. It returns a list of API key objects
    containing the key ID and creation time for each API key.
    """