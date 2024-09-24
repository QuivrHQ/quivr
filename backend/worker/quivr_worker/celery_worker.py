import asyncio
import os
from uuid import UUID

from celery.signals import worker_process_init
from dotenv import load_dotenv
from quivr_api.celery_config import celery
from quivr_api.logger import get_logger
from quivr_api.models.settings import settings
from quivr_api.modules.brain.integrations.Notion.Notion_connector import NotionConnector
from quivr_api.modules.brain.repository.brains_vectors import BrainsVectors
from quivr_api.modules.brain.service.brain_service import BrainService
from quivr_api.modules.dependencies import get_supabase_client
from quivr_api.modules.knowledge.dto.outputs import KnowledgeDTO
from quivr_api.modules.knowledge.repository.storage import SupabaseS3Storage
from quivr_api.modules.notification.service.notification_service import (
    NotificationService,
)
from quivr_api.modules.sync.service.sync_notion import SyncNotionService
from quivr_api.utils.telemetry import maybe_send_telemetry
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from quivr_worker.check_premium import check_is_premium
from quivr_worker.process.processor import KnowledgeProcessor, build_processor_services
from quivr_worker.syncs.process_active_syncs import (
    process_notion_sync,
)
from quivr_worker.syncs.store_notion import fetch_and_store_notion_files_async
from quivr_worker.utils import _patch_json

load_dotenv()

get_logger("quivr_core")
logger = get_logger("celery_worker")
_patch_json()


# FIXME: load at init time
# Services
supabase_client = get_supabase_client()
# document_vector_store = get_documents_vector_store()
notification_service = NotificationService()
brain_service = BrainService()
brain_vectors = BrainsVectors()
storage = SupabaseS3Storage()
notion_service: SyncNotionService | None = None
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


@celery.task(
    retries=3,
    default_retry_delay=1,
    name="process_file_task",
    autoretry_for=(Exception,),
    dont_autoretry_for=(FileExistsError,),
)
def process_file_task(
    knowledge_dto: KnowledgeDTO,
    notification_id: UUID | None = None,
):
    if async_engine is None:
        init_worker()

    logger.info(
        f"Task process_file started for knowledge_id={knowledge_dto.id}, notification_id={notification_id}"
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(aprocess_file_task(knowledge_dto))


async def aprocess_file_task(knowledge_dto: KnowledgeDTO):
    global async_engine
    assert async_engine
    async with build_processor_services(async_engine) as processor_services:
        km_processor = KnowledgeProcessor(processor_services)
        await km_processor.process_knowledge(knowledge_dto)


@celery.task(name="NotionConnectorLoad")
def process_integration_brain_created_initial_load(brain_id, user_id):
    notion_connector = NotionConnector(brain_id=brain_id, user_id=user_id)
    pages = notion_connector.load()
    logger.info("Notion pages: ", len(pages))


@celery.task
def process_integration_brain_sync_user_brain(brain_id, user_id):
    notion_connector = NotionConnector(brain_id=brain_id, user_id=user_id)
    notion_connector.poll()


@celery.task
def ping_telemetry():
    maybe_send_telemetry("ping", {"ping": "pong"})


@celery.task(name="check_is_premium_task")
def check_is_premium_task():
    check_is_premium(supabase_client)


@celery.task(name="process_notion_sync_task")
def process_notion_sync_task():
    global async_engine
    assert async_engine
    loop = asyncio.get_event_loop()
    loop.run_until_complete(process_notion_sync(async_engine))


@celery.task(name="fetch_and_store_notion_files_task")
def fetch_and_store_notion_files_task(access_token: str, user_id: UUID):
    if async_engine is None:
        init_worker()
    assert async_engine
    logger.debug("Fetching and storing Notion files")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        fetch_and_store_notion_files_async(async_engine, access_token, user_id)
    )


# from celery.schedules import crontab

# celery.conf.beat_schedule = {
#     "ping_telemetry": {
#         "task": f"{__name__}.ping_telemetry",
#         "schedule": crontab(minute="*/30", hour="*"),
#     },
#     "process_active_syncs": {
#         "task": "process_active_syncs_task",
#         "schedule": crontab(minute="*/1", hour="*"),
#     },
#     "process_premium_users": {
#         "task": "check_is_premium_task",
#         "schedule": crontab(minute="*/1", hour="*"),
#     },
#     "process_notion_sync": {
#         "task": "process_notion_sync_task",
#         "schedule": crontab(minute="0", hour="*/6"),
#     },
# }
