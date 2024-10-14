import asyncio
import os
from datetime import datetime
from typing import List, Tuple
from uuid import UUID

from fastapi import APIRouter, Depends, status

from quivr_api.logger import get_logger
from quivr_api.middlewares.auth import AuthBearer, get_current_user
from quivr_api.modules.dependencies import get_service
from quivr_api.modules.knowledge.entity.knowledge import KnowledgeDB, KnowledgeDTO
from quivr_api.modules.knowledge.service.knowledge_service import KnowledgeService
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
from quivr_api.modules.sync.entity.sync_models import SyncFile
from quivr_api.modules.sync.service.sync_service import SyncsService
from quivr_api.modules.user.entity.user_identity import UserIdentity

notification_service = NotificationService()

# Set environment variable for OAuthlib
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Initialize logger
logger = get_logger(__name__)

# Initialize sync service
get_sync_service = get_service(SyncsService)
get_knowledge_service = get_service(KnowledgeService)


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
async def get_all_sync_typs(current_user: UserIdentity = Depends(get_current_user)):
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
    syncs_service: SyncsService = Depends(get_sync_service),
):
    """
    Get syncs for the current user.

    Args:
        current_user (UserIdentity): The current authenticated user.

    Returns:
        List: A list of syncs for the user.
    """
    logger.debug(f"Fetching user syncs for user: {current_user.id}")
    return await syncs_service.get_user_syncs(current_user.id)


@sync_router.delete(
    "/sync/{sync_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(AuthBearer())],
    tags=["Sync"],
)
async def delete_user_sync(
    sync_id: int,
    current_user: UserIdentity = Depends(get_current_user),
    syncs_service: SyncsService = Depends(get_sync_service),
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
    response_model=List[KnowledgeDTO] | None,
    tags=["Sync"],
)
async def list_sync_files(
    sync_id: int,
    folder_id: str | None = None,
    current_user: UserIdentity = Depends(get_current_user),
    syncs_service: SyncsService = Depends(get_sync_service),
    knowledge_service: KnowledgeService = Depends(get_knowledge_service),
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
    logger.debug(f"Fetching files for user sync: {sync_id} for user: {current_user.id}")

    # TODO: check to see if this is inefficient
    # Gets knowledge for each call to list the files,
    # The logic is that getting from DB will be faster than provider repsonse ?
    # NOTE: asyncio.gather didn't correcly typecheck

    async def fetch_sync_knowledge(
        sync_id: int,
        user_id: UUID,
        folder_id: str | None,
    ) -> Tuple[dict[str, KnowledgeDB], List[SyncFile] | None]:
        map_knowledges_task = knowledge_service.map_syncs_knowledge_user(
            sync_id=sync_id, user_id=user_id
        )
        sync_files_task = syncs_service.get_files_folder_user_sync(
            sync_id,
            user_id,
            folder_id,
        )
        return await asyncio.gather(*[map_knowledges_task, sync_files_task])  # type: ignore  # noqa: F821

    sync = await syncs_service.get_sync_by_id(sync_id=sync_id)
    syncfile_to_knowledge, sync_files = await fetch_sync_knowledge(
        sync_id=sync_id,
        user_id=current_user.id,
        folder_id=folder_id,
    )
    if not sync_files:
        return None

    kms = []
    for file in sync_files:
        existing_km = syncfile_to_knowledge.get(file.id)
        if existing_km:
            kms.append(await existing_km.to_dto(get_children=False, get_parent=False))
        else:
            last_modified_at = (
                file.last_modified_at if file.last_modified_at else datetime.now()
            )
            kms.append(
                KnowledgeDTO(
                    id=None,
                    file_name=file.name,
                    is_folder=file.is_folder,
                    extension=file.extension,
                    source=sync.provider,
                    source_link=file.web_view_link,
                    user_id=current_user.id,
                    brains=[],
                    parent=None,
                    children=[],
                    # TODO: Handle a sync not added status
                    status=None,
                    # TODO: retrieve created at from sync provider
                    created_at=last_modified_at,
                    updated_at=last_modified_at,
                    sync_id=sync_id,
                    sync_file_id=file.id,
                )
            )
    return kms
