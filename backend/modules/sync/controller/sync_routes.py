import os
from typing import List

from fastapi import APIRouter, Depends, status
from logger import get_logger
from middlewares.auth import AuthBearer, get_current_user
from modules.sync.controller.azure_sync_routes import azure_sync_router
from modules.sync.controller.google_sync_routes import google_sync_router
from modules.sync.dto import SyncsDescription
from modules.sync.dto.inputs import SyncsActiveInput, SyncsActiveUpdateInput
from modules.sync.dto.outputs import AuthMethodEnum
from modules.sync.entity.sync import SyncsActive
from modules.sync.service.sync_service import SyncService, SyncUserService
from modules.user.entity.user_identity import UserIdentity

# Set environment variable for OAuthlib
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Initialize logger
logger = get_logger(__name__)

# Initialize sync service
sync_service = SyncService()
sync_user_service = SyncUserService()

# Initialize API router
sync_router = APIRouter()

# Add Google routes here
sync_router.include_router(google_sync_router)
sync_router.include_router(azure_sync_router)


# Google sync description
google_sync = SyncsDescription(
    name="Google",
    description="Sync your Google Drive with Quivr",
    auth_method=AuthMethodEnum.URI_WITH_CALLBACK,
)

azure_sync = SyncsDescription(
    name="Azure",
    description="Sync your Azure Drive with Quivr",
    auth_method=AuthMethodEnum.URI_WITH_CALLBACK,
)


@sync_router.get(
    "/sync/all",
    response_model=List[SyncsDescription],
    dependencies=[Depends(AuthBearer())],
    tags=["Sync"],
)
async def get_syncs(current_user: UserIdentity = Depends(get_current_user)):
    """
    Get all available sync descriptions.

    Args:
        current_user (UserIdentity): The current authenticated user.

    Returns:
        List[SyncsDescription]: A list of available sync descriptions.
    """
    logger.debug(f"Fetching all sync descriptions for user: {current_user.id}")
    return [google_sync, azure_sync]


@sync_router.get(
    "/sync",
    dependencies=[Depends(AuthBearer())],
    tags=["Sync"],
)
async def get_user_syncs(current_user: UserIdentity = Depends(get_current_user)):
    """
    Get syncs for the current user.

    Args:
        current_user (UserIdentity): The current authenticated user.

    Returns:
        List: A list of syncs for the user.
    """
    logger.debug(f"Fetching user syncs for user: {current_user.id}")
    return sync_user_service.get_syncs_user(str(current_user.id))


@sync_router.post(
    "/sync/active",
    response_model=SyncsActive,
    dependencies=[Depends(AuthBearer())],
    tags=["Sync"],
)
async def create_sync_active(
    sync_active_input: SyncsActiveInput,
    current_user: UserIdentity = Depends(get_current_user),
):
    """
    Create a new active sync for the current user.

    Args:
        sync_active_input (SyncsActiveInput): The sync active input data.
        current_user (UserIdentity): The current authenticated user.

    Returns:
        SyncsActive: The created sync active data.
    """
    logger.debug(
        f"Creating active sync for user: {current_user.id} with data: {sync_active_input}"
    )
    return sync_service.create_sync_active(sync_active_input, str(current_user.id))


@sync_router.put(
    "/sync/active/{sync_id}",
    response_model=SyncsActive,
    dependencies=[Depends(AuthBearer())],
    tags=["Sync"],
)
async def update_sync_active(
    sync_id: str,
    sync_active_input: SyncsActiveUpdateInput,
    current_user: UserIdentity = Depends(get_current_user),
):
    """
    Update an existing active sync for the current user.

    Args:
        sync_id (str): The ID of the active sync to update.
        sync_active_input (SyncsActiveUpdateInput): The updated sync active input data.
        current_user (UserIdentity): The current authenticated user.

    Returns:
        SyncsActive: The updated sync active data.
    """
    logger.debug(
        f"Updating active sync for user: {current_user.id} with data: {sync_active_input}"
    )
    return sync_service.update_sync_active(sync_id, sync_active_input)


@sync_router.delete(
    "/sync/active/{sync_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(AuthBearer())],
    tags=["Sync"],
)
async def delete_sync_active(
    sync_id: str, current_user: UserIdentity = Depends(get_current_user)
):
    """
    Delete an existing active sync for the current user.

    Args:
        sync_id (str): The ID of the active sync to delete.
        current_user (UserIdentity): The current authenticated user.

    Returns:
        None
    """
    logger.debug(
        f"Deleting active sync for user: {current_user.id} with sync ID: {sync_id}"
    )
    sync_service.delete_sync_active(sync_id, str(current_user.id))
    return None


@sync_router.get(
    "/sync/active",
    response_model=List[SyncsActive],
    dependencies=[Depends(AuthBearer())],
    tags=["Sync"],
)
async def get_active_syncs_for_user(
    current_user: UserIdentity = Depends(get_current_user),
):
    """
    Get all active syncs for the current user.

    Args:
        current_user (UserIdentity): The current authenticated user.

    Returns:
        List[SyncsActive]: A list of active syncs for the current user.
    """
    logger.debug(f"Fetching active syncs for user: {current_user.id}")
    return sync_service.get_syncs_active(str(current_user.id))


@sync_router.get(
    "/sync/{sync_id}/files",
    dependencies=[Depends(AuthBearer())],
    tags=["Sync"],
)
async def get_files_folder_user_sync(
    user_sync_id: int,
    folder_id: str = None,
    current_user: UserIdentity = Depends(get_current_user),
):
    """
    Get files for an active sync.

    Args:
        sync_id (str): The ID of the active sync.
        folder_id (str): The ID of the folder to get files from.
        current_user (UserIdentity): The current authenticated user.

    Returns:
        SyncsActive: The active sync data.
    """
    logger.debug(
        f"Fetching files for user sync: {user_sync_id} for user: {current_user.id}"
    )
    return sync_user_service.get_files_folder_user_sync(
        user_sync_id, str(current_user.id), folder_id
    )


@sync_router.get(
    "/sync/active/interval",
    dependencies=[Depends(AuthBearer())],
    tags=["Sync"],
)
async def get_syncs_active_in_interval() -> List[SyncsActive]:
    """
    Get all active syncs that need to be synced.

    Returns:
        List: A list of active syncs that need to be synced.
    """
    logger.debug("Fetching active syncs in interval")
    return await sync_service.get_syncs_active_in_interval()
