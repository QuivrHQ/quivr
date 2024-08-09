from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncGenerator
from uuid import UUID

from notion_client import Client
from quivr_api.celery_config import celery
from quivr_api.logger import get_logger
from quivr_api.modules.brain.repository.brains_vectors import BrainsVectors
from quivr_api.modules.knowledge.repository.storage import Storage
from quivr_api.modules.knowledge.service.knowledge_service import KnowledgeService
from quivr_api.modules.notification.service.notification_service import (
    NotificationService,
)
from quivr_api.modules.sync.entity.sync_models import SyncsActive
from quivr_api.modules.sync.repository.sync_files import SyncFilesRepository
from quivr_api.modules.sync.repository.sync_repository import NotionRepository
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

celery_inspector = celery.control.inspect()

logger = get_logger("celery_worker")


@dataclass
class SyncServices:
    async_engine: AsyncEngine
    knowledge_service: KnowledgeService
    sync_active_service: SyncService
    sync_user_service: SyncUserService
    sync_files_repo_service: SyncFilesRepository
    notification_service: NotificationService
    brain_vectors: BrainsVectors
    storage: Storage


@asynccontextmanager
async def build_syncs_utils(
    deps: SyncServices,
) -> AsyncGenerator[dict[str, SyncUtils], None]:
    async with AsyncSession(
        deps.async_engine, expire_on_commit=False, autoflush=False
    ) as session:
        try:
            # TODO pass services from celery_worker
            notion_repository = NotionRepository(session)
            notion_service = SyncNotionService(notion_repository)

            mapping_sync_utils = {}
            for provider_name, sync_cloud in [
                ("google", GoogleDriveSync()),
                ("azure", AzureDriveSync()),
                ("dropbox", DropboxSync()),
                ("github", GitHubSync()),
                (
                    "notion",
                    NotionSync(notion_service=notion_service),
                ),  # Fixed duplicate "github" key
            ]:
                provider_sync_util = SyncUtils(
                    sync_user_service=deps.sync_user_service,
                    sync_active_service=deps.sync_active_service,
                    sync_files_repo=deps.sync_files_repo_service,
                    storage=deps.storage,
                    sync_cloud=sync_cloud,
                    notification_service=deps.notification_service,
                    brain_vectors=deps.brain_vectors,
                    knowledge_service=deps.knowledge_service,
                )
                mapping_sync_utils[provider_name] = provider_sync_util

            yield mapping_sync_utils
        finally:
            # No need to close the session explicitly as it's handled by the context manager
            pass


async def process_sync(sync: SyncsActive, services: SyncServices):
    async with build_syncs_utils(services) as mapping_syncs_utils:
        try:
            user_sync = services.sync_user_service.get_sync_user_by_id(
                sync.syncs_user_id
            )
            # NOTE: remove notification id
            services.notification_service.remove_notification_by_id(
                sync.notification_id
            )
            assert user_sync, f"No user sync found for active sync: {sync}"
            sync_util = mapping_syncs_utils[user_sync.provider.lower()]
            await sync_util.sync(sync_active=sync, user_sync=user_sync)
        except KeyError as e:
            logger.error(
                f"Provider not supported: {e}",
            )
        except Exception as e:
            logger.error(f"Error syncing: {e}")


async def process_all_active_syncs(sync_services: SyncServices):
    async with build_syncs_utils(sync_services) as mapping_sync_utils:
        await _process_all_active_syncs(
            sync_active_service=sync_services.sync_active_service,
            sync_user_service=sync_services.sync_user_service,
            mapping_syncs_utils=mapping_sync_utils,
            notification_service=sync_services.notification_service,
        )


async def _process_all_active_syncs(
    sync_active_service: SyncService,
    sync_user_service: SyncUserService,
    mapping_syncs_utils: dict[str, SyncUtils],
    notification_service: NotificationService,
):
    active_syncs = await sync_active_service.get_syncs_active_in_interval()
    logger.debug(f"Found active syncs: {active_syncs}")
    for sync in active_syncs:
        try:
            user_sync = sync_user_service.get_sync_user_by_id(sync.syncs_user_id)
            # TODO: this should be global
            # NOTE: Remove the global notification
            notification_service.remove_notification_by_id(sync.notification_id)
            assert user_sync, f"No user sync found for active sync: {sync}"
            sync_util = mapping_syncs_utils[user_sync.provider.lower()]
            await sync_util.sync(sync_active=sync, user_sync=user_sync)
        except KeyError as e:
            logger.error(
                f"Provider not supported: {e}",
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

        # TODO: Add state in sync_user to check if the same fetching is running
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
