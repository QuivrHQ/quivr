from secrets import token_hex
from typing import List
from uuid import uuid4

from fastapi import APIRouter, Depends
from quivr_api.logger import get_logger
from quivr_api.middlewares.auth import AuthBearer, get_current_user
from quivr_api.modules.api_key.dto.outputs import ApiKeyInfo
from quivr_api.modules.api_key.entity.api_key import ApiKey
from quivr_api.modules.api_key.repository.api_keys import ApiKeys
from quivr_api.modules.user.entity.user_identity import UserIdentity

logger = get_logger(__name__)


api_key_router = APIRouter()

api_keys_repository = ApiKeys()


@api_key_router.post(
    "/api-key",
    response_model=ApiKey,
    dependencies=[Depends(AuthBearer())],
    tags=["API Key"],
)
async def create_api_key(current_user: UserIdentity = Depends(get_current_user)):
    """
    Create new API key for the current user.

    - `current_user`: The current authenticated user.
    - Returns the newly created API key.

    This endpoint generates a new API key for the current user. The API key is stored in the database and associated with
    the user. It returns the newly created API key.
    """

    new_key_id = uuid4()
    new_api_key = token_hex(16)

    try:
        # Attempt to insert new API key into database
        response = api_keys_repository.create_api_key(
            new_key_id, new_api_key, current_user.id, "api_key", 30, False
        )
    except Exception as e:
        logger.error(f"Error creating new API key: {e}")
        return {"api_key": "Error creating new API key."}
    logger.info(f"Created new API key for user {current_user.email}.")

    return response  # type: ignore


@api_key_router.delete(
    "/api-key/{key_id}", dependencies=[Depends(AuthBearer())], tags=["API Key"]
)
async def delete_api_key(
    key_id: str, current_user: UserIdentity = Depends(get_current_user)
):
    """
    Delete (deactivate) an API key for the current user.

    - `key_id`: The ID of the API key to delete.

    This endpoint deactivates and deletes the specified API key associated with the current user. The API key is marked
    as inactive in the database.

    """
    api_keys_repository.delete_api_key(key_id, current_user.id)

    return {"message": "API key deleted."}


@api_key_router.get(
    "/api-keys",
    response_model=List[ApiKeyInfo],
    dependencies=[Depends(AuthBearer())],
    tags=["API Key"],
)
async def get_api_keys(current_user: UserIdentity = Depends(get_current_user)):
    """
    Get all active API keys for the current user.

    - `current_user`: The current authenticated user.
    - Returns a list of active API keys with their IDs and creation times.

    This endpoint retrieves all the active API keys associated with the current user. It returns a list of API key objects
    containing the key ID and creation time for each API key.
    """
    response = api_keys_repository.get_user_api_keys(current_user.id)
    return response.data
