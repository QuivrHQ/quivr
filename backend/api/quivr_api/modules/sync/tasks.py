import asyncio
import os
import uuid

from celery.signals import worker_process_init
from notion_client import Client
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_api.celery_config import celery
from quivr_api.logger import get_logger
from quivr_api.models.settings import settings
from quivr_api.modules.knowledge.repository.storage import Storage
from quivr_api.modules.notification.service.notification_service import (
    NotificationService,
)
from quivr_api.modules.sync.repository.sync import NotionRepository
from quivr_api.modules.sync.repository.sync_files import SyncFiles
from quivr_api.modules.sync.service.sync_notion import (
    SyncNotionService,
    fetch_notion_pages,
    update_notion_pages,
)
from quivr_api.modules.sync.service.sync_service import SyncService, SyncUserService
from quivr_api.modules.sync.utils.sync import (
    AzureDriveSync,
    DropboxSync,
    GoogleDriveSync,
    NotionSync,
)
from quivr_api.modules.sync.utils.syncutils import SyncUtils

notification_service = NotificationService()
celery_inspector = celery.control.inspect()

logger = get_logger(__name__)

async_engine: AsyncEngine | None = None


@worker_process_init.connect
def init_worker(**kwargs):
    global async_engine
    if not async_engine:
        async_engine = create_async_engine(
            settings.pg_database_async_url,
            echo=True if os.getenv("ORM_DEBUG") else False,
            future=True,
            # NOTE: pessimistic bound on
            pool_pre_ping=True,
            pool_size=10,  # NOTE: no bouncer for now, if 6 process workers => 6
            pool_recycle=1800,
        )


@celery.task(name="process_sync_active")
def process_sync_active():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_process_sync_active())


async def _process_sync_active():
    assert async_engine

    async with AsyncSession(
        async_engine, expire_on_commit=False, autoflush=False
    ) as session:
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

        notion_repository = NotionRepository(session)
        notion_service = SyncNotionService(notion_repository)
        notion_sync_utils = SyncUtils(
            sync_user_service=sync_user_service,
            sync_active_service=sync_active_service,
            sync_files_repo=sync_files_repo_service,
            storage=storage,
            sync_cloud=NotionSync(notion_service=notion_service),
        )

        active = await sync_active_service.get_syncs_active_in_interval()

        for sync in active:
            try:
                details_user_sync = sync_user_service.get_sync_user_by_id(
                    sync.syncs_user_id
                )
                if details_user_sync["provider"].lower() == "google":
                    await google_sync_utils.sync(
                        sync_active_id=sync.id, user_id=sync.user_id
                    )
                elif details_user_sync["provider"].lower() == "azure":
                    await azure_sync_utils.sync(
                        sync_active_id=sync.id, user_id=sync.user_id
                    )
                elif details_user_sync["provider"].lower() == "dropbox":
                    await dropbox_sync_utils.sync(
                        sync_active_id=sync.id, user_id=sync.user_id
                    )
                elif details_user_sync["provider"].lower() == "notion":
                    await notion_sync_utils.sync(
                        sync_active_id=sync.id,
                        user_id=sync.user_id,
                        notion_service=notion_service,
                    )
                else:
                    logger.info(
                        "Provider not supported: %s", details_user_sync["provider"]
                    )
            except Exception as e:
                logger.error(f"Error syncing: {e}")
                continue


@celery.task(name="process_notion_sync")
def process_notion_sync():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_process_notion_sync())


async def _process_notion_sync():
    assert async_engine
    async with AsyncSession(
        async_engine, expire_on_commit=False, autoflush=False
    ) as session:
        sync_user_service = SyncUserService()

    notion_repository = NotionRepository(session)
    notion_service = SyncNotionService(notion_repository)

    # Get active tasks for all workers
    active_tasks = celery_inspector.active()
    is_uploading_task_running = any(
        "fetch_and_store_notion_files" in task
        for worker_tasks in active_tasks.values()
        for task in worker_tasks
    )
    if is_uploading_task_running:
        return None

    # get all notion syncs
    notion_syncs = sync_user_service.get_all_notion_user_syncs()
    for notion_sync in notion_syncs:
        user_id = notion_sync["user_id"]
        notion_client = Client(auth=notion_sync["credentials"]["access_token"])

        all_search_result = fetch_notion_pages(notion_client)
        all_db_pages = await notion_service.get_all_notion_files()
        await update_notion_pages(
            all_search_result, all_db_pages, notion_service, uuid.UUID(user_id)
        )
