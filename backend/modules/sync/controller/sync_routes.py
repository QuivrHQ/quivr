import os
from typing import List

from fastapi import APIRouter, Depends
from logger import get_logger
from middlewares.auth import AuthBearer, get_current_user
from modules.sync.controller.google_sync_routes import google_sync_router
from modules.sync.controller.azure_sync_routes import azure_sync_router
from modules.sync.dto import SyncsDescription
from modules.sync.dto.outputs import AuthMethodEnum
from modules.sync.service.sync_service import SyncService
from modules.user.entity.user_identity import UserIdentity

# Set environment variable for OAuthlib
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Initialize logger
logger = get_logger(__name__)

# Initialize sync service
sync_service = SyncService()

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
    return [google_sync]


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
    return sync_service.get_syncs_user(str(current_user.id))
