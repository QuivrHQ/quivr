import asyncio

from celery_config import celery
from logger import get_logger
from modules.knowledge.repository.storage import Storage
from modules.sync.repository.sync_files import SyncFiles
from modules.sync.service.sync_service import SyncService, SyncUserService
from modules.sync.utils.googleutils import GoogleSyncUtils
from modules.sync.utils.sharepointutils import AzureSyncUtils

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

    google_sync_utils = GoogleSyncUtils(
        sync_user_service=sync_user_service,
        sync_active_service=sync_active_service,
        sync_files_repo=sync_files_repo_service,
        storage=storage,
    )

    azure_sync_utils = AzureSyncUtils(
        sync_user_service=sync_user_service,
        sync_active_service=sync_active_service,
        sync_files_repo=sync_files_repo_service,
        storage=storage,
    )
    active = await sync_active_service.get_syncs_active_in_interval()

    for sync in active:
        details_user_sync = sync_user_service.get_sync_user_by_id(sync.syncs_user_id)
        if details_user_sync["provider"].lower() == "google":
            await google_sync_utils.sync(sync_active_id=sync.id, user_id=sync.user_id)
        elif details_user_sync["provider"].lower() == "azure":
            await azure_sync_utils.sync(sync_active_id=sync.id, user_id=sync.user_id)
        else:
            logger.info("Provider not supported: %s", details_user_sync["provider"])
