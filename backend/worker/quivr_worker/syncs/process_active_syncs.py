from datetime import datetime, timedelta
from uuid import UUID

from notion_client import Client
from quivr_api.celery_config import celery
from quivr_api.logger import get_logger
from quivr_api.modules.notification.service.notification_service import (
    NotificationService,
)
from quivr_api.modules.sync.entity.sync_models import SyncsActive
from quivr_api.modules.sync.repository.sync_repository import NotionRepository
from quivr_api.modules.sync.service.sync_notion import (
    SyncNotionService,
    fetch_limit_notion_pages,
    update_notion_pages,
)
from quivr_api.modules.sync.service.sync_service import SyncService, SyncUserService
from quivr_api.modules.sync.utils.syncutils import SyncUtils
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import text
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_worker.syncs.utils import SyncServices, build_syncs_utils

celery_inspector = celery.control.inspect()

logger = get_logger("celery_worker")


async def process_sync(
    sync: SyncsActive,
    files_ids: list[str],
    folder_ids: list[str],
    services: SyncServices,
):
    async with build_syncs_utils(services) as mapping_syncs_utils:
        try:
            user_sync = services.sync_user_service.get_sync_user_by_id(
                sync.syncs_user_id
            )
            services.notification_service.remove_notification_by_id(
                sync.notification_id
            )
            assert user_sync, f"No user sync found for active sync: {sync}"
            sync_util = mapping_syncs_utils[user_sync.provider.lower()]
            await sync_util.direct_sync(
                sync_active=sync,
                user_sync=user_sync,
                files_ids=files_ids,
                folder_ids=folder_ids,
            )
        except KeyError as e:
            logger.error(
                f"Provider not supported: {e}",
            )
        except Exception as e:
            logger.error(f"Error direct sync for {sync.id}: {e}")
            raise e


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
    try:
        async with AsyncSession(
            async_engine, expire_on_commit=False, autoflush=False
        ) as session:
            await session.execute(
                text("SET SESSION idle_in_transaction_session_timeout = '5min';")
            )
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

                # TODO: fetch last_sync_time from table
                pages_to_update = fetch_limit_notion_pages(
                    notion_client,
                    datetime.now() - timedelta(hours=6),
                )
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
            await session.commit()
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()
