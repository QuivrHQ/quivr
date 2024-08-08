from uuid import UUID

from notion_client import Client
from quivr_api.celery_config import celery
from quivr_api.logger import get_logger
from quivr_api.modules.knowledge.repository.knowledges import KnowledgeRepository
from quivr_api.modules.knowledge.repository.storage import Storage
from quivr_api.modules.knowledge.service.knowledge_service import KnowledgeService
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
    GitHubSync,
    GoogleDriveSync,
    NotionSync,
)
from quivr_api.modules.sync.utils.syncutils import SyncUtils
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession

notification_service = NotificationService()
celery_inspector = celery.control.inspect()

logger = get_logger(__name__)


async def process_all_syncs(
    async_engine: AsyncEngine,
    sync_active_service: SyncService,
    sync_user_service: SyncUserService,
    sync_files_repo_service: SyncFiles,
    storage: Storage,
):
    async with AsyncSession(
        async_engine, expire_on_commit=False, autoflush=False
    ) as session:
        sync_active_service = SyncService()
        sync_user_service = SyncUserService()
        sync_files_repo_service = SyncFiles()
        knowledge_repository = KnowledgeRepository(session)
        knowledge_service = KnowledgeService(knowledge_repository)
        storage = Storage()

        google_sync_utils = SyncUtils(
            sync_user_service=sync_user_service,
            sync_active_service=sync_active_service,
            sync_files_repo=sync_files_repo_service,
            storage=storage,
            sync_cloud=GoogleDriveSync(),
            knowledge_service=knowledge_service,
        )

        azure_sync_utils = SyncUtils(
            sync_user_service=sync_user_service,
            sync_active_service=sync_active_service,
            sync_files_repo=sync_files_repo_service,
            storage=storage,
            sync_cloud=AzureDriveSync(),
            knowledge_service=knowledge_service,
        )

        dropbox_sync_utils = SyncUtils(
            sync_user_service=sync_user_service,
            sync_active_service=sync_active_service,
            sync_files_repo=sync_files_repo_service,
            storage=storage,
            sync_cloud=DropboxSync(),
            knowledge_service=knowledge_service,
        )
        github_sync_utils = SyncUtils(
            sync_user_service=sync_user_service,
            sync_active_service=sync_active_service,
            sync_files_repo=sync_files_repo_service,
            storage=storage,
            sync_cloud=GitHubSync(),
            knowledge_service=knowledge_service,
        )

        active = await sync_active_service.get_syncs_active_in_interval()

        notion_repository = NotionRepository(session)
        notion_service = SyncNotionService(notion_repository)

        notion_sync_utils = SyncUtils(
            sync_user_service=sync_user_service,
            sync_active_service=sync_active_service,
            sync_files_repo=sync_files_repo_service,
            storage=storage,
            sync_cloud=NotionSync(notion_service=notion_service),
            knowledge_service=knowledge_service,
        )

        active = await sync_active_service.get_syncs_active_in_interval()

        # FIXME: THIS SHOULD BE a separate function
        for sync in active:
            try:
                details_user_sync = sync_user_service.get_sync_user_by_id(
                    sync.syncs_user_id
                )
                assert details_user_sync
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
                elif details_user_sync["provider"].lower() == "github":
                    await github_sync_utils.sync(
                        sync_active_id=sync.id, user_id=sync.user_id
                    )
                else:
                    logger.info(
                        "Provider not supported: %s", details_user_sync["provider"]
                    )
            except Exception as e:
                logger.error(f"Error syncing: {e}")
                continue


async def process_notion_sync(
    async_engine: AsyncEngine,
):
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

        # Get all notion syncs
        notion_syncs = sync_user_service.get_all_notion_user_syncs()
        for notion_sync in notion_syncs:
            user_id = notion_sync["user_id"]
            notion_client = Client(auth=notion_sync["credentials"]["access_token"])

            pages_to_update = fetch_notion_pages(notion_client, notion_sync=notion_sync)
            logger.debug("Number of pages to update: %s", len(pages_to_update))
            if not pages_to_update:
                logger.info("No pages to update")
                continue

            await update_notion_pages(
                notion_service,
                pages_to_update,
                UUID(user_id),
                notion_client,  # type: ignore
            )
