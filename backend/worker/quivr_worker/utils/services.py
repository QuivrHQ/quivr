from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncGenerator

from quivr_api.logger import get_logger
from quivr_api.modules.dependencies import get_supabase_async_client
from quivr_api.modules.knowledge.repository.knowledges import KnowledgeRepository
from quivr_api.modules.knowledge.repository.storage import SupabaseS3Storage
from quivr_api.modules.knowledge.service.knowledge_service import KnowledgeService
from quivr_api.modules.sync.dto.outputs import SyncProvider
from quivr_api.modules.sync.repository.sync_repository import SyncsRepository
from quivr_api.modules.sync.service.sync_service import SyncsService
from quivr_api.modules.sync.utils.sync import (
    BaseSync,
)
from quivr_api.modules.vector.repository.vectors_repository import VectorRepository
from quivr_api.modules.vector.service.vector_service import VectorService
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import text
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_worker.process.utils import (
    build_syncprovider_mapping,
)

logger = get_logger("celery_worker")


@dataclass
class ProcessorServices:
    sync_service: SyncsService
    vector_service: VectorService
    knowledge_service: KnowledgeService
    syncprovider_mapping: dict[SyncProvider, BaseSync]


@asynccontextmanager
async def _start_session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        try:
            await session.execute(
                text("SET SESSION idle_in_transaction_session_timeout = '5min';")
            )
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


@asynccontextmanager
async def build_processor_services(
    engine: AsyncEngine,
) -> AsyncGenerator[ProcessorServices, None]:
    async_client = await get_supabase_async_client()
    storage = SupabaseS3Storage(async_client)
    try:
        async with _start_session(engine) as session:
            vector_repository = VectorRepository(session)
            vector_service = VectorService(vector_repository)
            knowledge_repository = KnowledgeRepository(session)
            knowledge_service = KnowledgeService(knowledge_repository, storage=storage)
            sync_repository = SyncsRepository(session)
            sync_service = SyncsService(sync_repository)
            yield ProcessorServices(
                knowledge_service=knowledge_service,
                vector_service=vector_service,
                sync_service=sync_service,
                syncprovider_mapping=build_syncprovider_mapping(),
            )
    finally:
        logger.info("Closing processor services")
