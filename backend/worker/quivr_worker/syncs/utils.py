from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncGenerator

from quivr_api.celery_config import celery
from quivr_api.logger import get_logger
from quivr_api.modules.brain.repository.brains_vectors import BrainsVectors
from quivr_api.modules.knowledge.repository.knowledges import KnowledgeRepository
from quivr_api.modules.knowledge.repository.storage import Storage
from quivr_api.modules.knowledge.service.knowledge_service import KnowledgeService
from quivr_api.modules.notification.service.notification_service import (
    NotificationService,
)
from quivr_api.modules.sync.repository.sync_files import SyncFilesRepository
from quivr_api.modules.sync.repository.sync_repository import NotionRepository
from quivr_api.modules.sync.service.sync_notion import (
    SyncNotionService,
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
        # TODO pass services from celery_worker
        notion_repository = NotionRepository(session)
        notion_service = SyncNotionService(notion_repository)
        knowledge_service = KnowledgeService(KnowledgeRepository(session))

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
                sync_cloud=sync_cloud,
                notification_service=deps.notification_service,
                brain_vectors=deps.brain_vectors,
                knowledge_service=knowledge_service,
            )
            mapping_sync_utils[provider_name] = provider_sync_util

        yield mapping_sync_utils
