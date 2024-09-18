import os
from typing import List

from fastapi import APIRouter, Depends, status

from quivr_api.logger import get_logger
from quivr_api.middlewares.auth import AuthBearer, get_current_user
from quivr_api.modules.dependencies import get_service
from quivr_api.modules.notification.service.notification_service import (
    NotificationService,
)
from quivr_api.modules.sync.controller.azure_sync_routes import azure_sync_router
from quivr_api.modules.sync.controller.dropbox_sync_routes import dropbox_sync_router
from quivr_api.modules.sync.controller.github_sync_routes import github_sync_router
from quivr_api.modules.sync.controller.google_sync_routes import google_sync_router
from quivr_api.modules.sync.controller.notion_sync_routes import notion_sync_router
from quivr_api.modules.sync.dto import SyncsDescription
from quivr_api.modules.sync.dto.outputs import AuthMethodEnum
from quivr_api.modules.sync.service.sync_service import SyncsService
from quivr_api.modules.user.entity.user_identity import UserIdentity

notification_service = NotificationService()

# Set environment variable for OAuthlib
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Initialize logger
logger = get_logger(__name__)

# Initialize sync service
syncs_service_dep = get_service(SyncsService)


# Initialize API router
sync_router = APIRouter()

# Add Google routes here
sync_router.include_router(google_sync_router)
sync_router.include_router(azure_sync_router)
sync_router.include_router(github_sync_router)
sync_router.include_router(dropbox_sync_router)
sync_router.include_router(notion_sync_router)


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

dropbox_sync = SyncsDescription(
    name="DropBox",
    description="Sync your DropBox Drive with Quivr",
    auth_method=AuthMethodEnum.URI_WITH_CALLBACK,
)

notion_sync = SyncsDescription(
    name="Notion",
    description="Sync your Notion with Quivr",
    auth_method=AuthMethodEnum.URI_WITH_CALLBACK,
)

github_sync = SyncsDescription(
    name="GitHub",
    description="Sync your GitHub Drive with Quivr",
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
    return [google_sync, azure_sync, dropbox_sync, notion_sync]


@sync_router.get(
    "/sync",
    dependencies=[Depends(AuthBearer())],
    tags=["Sync"],
)
async def get_user_syncs(
    current_user: UserIdentity = Depends(get_current_user),
    syncs_service: SyncsService = Depends(syncs_service_dep),
):
    """
    Get syncs for the current user.

    Args:
        current_user (UserIdentity): The current authenticated user.

    Returns:
        List: A list of syncs for the user.
    """
    logger.debug(f"Fetching user syncs for user: {current_user.id}")
    return await syncs_service.get_syncs(current_user.id)


@sync_router.delete(
    "/sync/{sync_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(AuthBearer())],
    tags=["Sync"],
)
async def delete_user_sync(
    sync_id: int,
    current_user: UserIdentity = Depends(get_current_user),
    syncs_service: SyncsService = Depends(syncs_service_dep),
):
    """
    Delete a sync for the current user.

    Args:
        sync_id (int): The ID of the sync to delete.
        current_user (UserIdentity): The current authenticated user.

    Returns:
        None
    """
    logger.debug(
        f"Deleting user sync for user: {current_user.id} with sync ID: {sync_id}"
    )
    await syncs_service.delete_sync(sync_id, current_user.id)
    return None


@sync_router.get(
    "/sync/{sync_id}/files",
    dependencies=[Depends(AuthBearer())],
    tags=["Sync"],
)
async def get_files_folder_user_sync(
    user_sync_id: int,
    folder_id: str | None = None,
    current_user: UserIdentity = Depends(get_current_user),
    syncs_service: SyncsService = Depends(syncs_service_dep),
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
    return await syncs_service.get_files_folder_user_sync(
        user_sync_id,
        current_user.id,
        folder_id,
    )
