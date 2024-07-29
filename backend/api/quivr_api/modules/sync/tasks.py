import asyncio

from quivr_api.celery_config import celery
from quivr_api.logger import get_logger
from quivr_api.modules.knowledge.repository.storage import Storage
from quivr_api.modules.notification.service.notification_service import (
    NotificationService,
)
from quivr_api.modules.sync.repository.sync_files import SyncFiles
from quivr_api.modules.sync.service.sync_service import SyncService, SyncUserService
from quivr_api.modules.sync.utils.sync import (
    AzureDriveSync,
    DropboxSync,
    GitHubSync,
    GoogleDriveSync,
)
from quivr_api.modules.sync.utils.syncutils import SyncUtils

notification_service = NotificationService()


logger = get_logger(__name__)


@celery.task(name="process_sync_active")
def process_sync_active():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_process_sync_active())


async def _process_sync_active():
    sync_active_service = SyncService()
    sync_user_service = SyncUserService()
    sync_files_repo_service = SyncFiles()
    storage = Storage()

    google_sync_utils = SyncUtils(
        sync_user_service=sync_user_service,
        sync_active_service=sync_active_service,
        sync_files_repo=sync_files_repo_service,
        storage=storage,
        sync_cloud=GoogleDriveSync(),
    )

    azure_sync_utils = SyncUtils(
        sync_user_service=sync_user_service,
        sync_active_service=sync_active_service,
        sync_files_repo=sync_files_repo_service,
        storage=storage,
        sync_cloud=AzureDriveSync(),
    )

    dropbox_sync_utils = SyncUtils(
        sync_user_service=sync_user_service,
        sync_active_service=sync_active_service,
        sync_files_repo=sync_files_repo_service,
        storage=storage,
        sync_cloud=DropboxSync(),
    )

    github_sync_utils = SyncUtils(
        sync_user_service=sync_user_service,
        sync_active_service=sync_active_service,
        sync_files_repo=sync_files_repo_service,
        storage=storage,
        sync_cloud=GitHubSync(),
    )

    active = await sync_active_service.get_syncs_active_in_interval()

    for sync in active:
        try:
            details_user_sync = sync_user_service.get_sync_user_by_id(
                sync.syncs_user_id
            )
            sync_active = None
            if details_user_sync is None:
                continue
            else:
                sync_active = sync_active_service.get_details_sync_active(sync.id)
                notification_service.remove_notification_by_id(
                    sync_active["notification_id"],
                )
            if details_user_sync["provider"].lower() == "google":
                await google_sync_utils.sync(
                    sync_active_id=sync.id, user_id=sync.user_id
                )
            elif details_user_sync["provider"].lower() == "azure":
                await azure_sync_utils.sync(
                    sync_active_id=sync.id, user_id=sync.user_id
                )
            elif details_user_sync["provider"].lower() == "github":
                await github_sync_utils.sync(
                    sync_active_id=sync.id, user_id=sync.user_id
                )
            elif details_user_sync["provider"].lower() == "dropbox":
                await dropbox_sync_utils.sync(
                    sync_active_id=sync.id, user_id=sync.user_id
                )

            else:
                logger.info("Provider not supported: %s", details_user_sync["provider"])
        except Exception as e:
            logger.error(f"Error syncing: {e}")
            continue
