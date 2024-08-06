import asyncio
import os
from uuid import UUID

from celery.schedules import crontab
from celery.signals import worker_process_init
from dotenv import load_dotenv
from notion_client import Client
from quivr_api.celery_config import celery
from quivr_api.logger import get_logger
from quivr_api.middlewares.auth.auth_bearer import AuthBearer
from quivr_api.models.settings import (
    get_documents_vector_store,
    get_supabase_client,
    settings,
)
from quivr_api.modules.brain.integrations.Notion.Notion_connector import NotionConnector
from quivr_api.modules.brain.service.brain_service import BrainService
from quivr_api.modules.brain.service.brain_vector_service import BrainVectorService
from quivr_api.modules.knowledge.repository.storage import Storage
from quivr_api.modules.notification.service.notification_service import (
    NotificationService,
)
from quivr_api.modules.sync.repository.sync import NotionRepository
from quivr_api.modules.sync.repository.sync_files import SyncFiles
from quivr_api.modules.sync.service.sync_notion import (
    SyncNotionService,
    fetch_notion_pages,
    store_notion_pages,
)
from quivr_api.modules.sync.service.sync_service import SyncService, SyncUserService
from quivr_api.utils.telemetry import maybe_send_telemetry
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_worker.check_premium import check_is_premium
from quivr_worker.process.process_s3_file import process_uploaded_file
from quivr_worker.process.process_url import process_url_func
from quivr_worker.syncs.process_active_syncs import (
    process_all_syncs,
    process_notion_sync,
)
from quivr_worker.utils import _patch_json

load_dotenv()

logger = get_logger("celery_worker")

# FIXME: load at init time
# Services
supabase_client = get_supabase_client()
document_vector_store = get_documents_vector_store()
notification_service = NotificationService()
sync_active_service = SyncService()
sync_user_service = SyncUserService()
sync_files_repo_service = SyncFiles()
storage = Storage()
brain_service = BrainService()
auth_bearer = AuthBearer()
notion_service: SyncNotionService | None = None
async_engine: AsyncEngine | None = None

_patch_json()


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
)
def process_file_task(
    file_name: str,
    file_original_name: str,
    brain_id: UUID,
    notification_id: UUID,
    knowledge_id: UUID,
    integration: str | None = None,
    integration_link: str | None = None,
    delete_file: bool = False,
):
    logger.info(
        f"Task process_file started for file_name={file_name}, knowledge_id={knowledge_id}, brain_id={brain_id}, notification_id={notification_id}"
    )

    brain_vector_service = BrainVectorService(brain_id)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        process_uploaded_file(
            supabase_client=supabase_client,
            brain_service=brain_service,
            brain_vector_service=brain_vector_service,
            document_vector_store=document_vector_store,
            file_name=file_name,
            brain_id=brain_id,
            file_original_name=file_original_name,
            knowledge_id=knowledge_id,
            integration=integration,
            integration_link=integration_link,
            delete_file=delete_file,
        )
    )


@celery.task(
    retries=3,
    default_retry_delay=1,
    name="process_crawl_and_notify",
    autoretry_for=(Exception,),
)
async def process_crawl_task(
    crawl_website_url: str,
    brain_id: UUID,
    knowledge_id: UUID,
    notification_id: UUID | None = None,
):
    logger.info(
        f"Task process_crawl_task started for url={crawl_website_url}, knowledge_id={knowledge_id}, brain_id={brain_id}, notification_id={notification_id}"
    )

    brain_vector_service = BrainVectorService(brain_id)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        process_url_func(
            url=crawl_website_url,
            brain_id=brain_id,
            knowledge_id=knowledge_id,
            brain_service=brain_service,
            brain_vector_service=brain_vector_service,
            document_vector_store=document_vector_store,
        )
    )


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


@celery.task(name="process_active_syncs_task")
def process_active_syncs_task():
    global async_engine
    assert async_engine
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        process_all_syncs(
            async_engine,
            sync_active_service,
            sync_user_service,
            sync_files_repo_service,
            storage,
        )
    )


@celery.task(name="process_notion_sync_task")
def process_notion_sync_task():
    global async_engine
    assert async_engine
    loop = asyncio.get_event_loop()
    loop.run_until_complete(process_notion_sync(async_engine))


@celery.task(name="fetch_and_store_notion_files")
def fetch_and_store_notion_files(access_token: str, user_id: UUID):
    if async_engine is None:
        init_worker()
    logger.debug("Fetching and storing Notion files")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_and_store_notion_files_async(access_token, user_id))


async def fetch_and_store_notion_files_async(access_token: str, user_id: UUID):
    global async_engine
    assert async_engine
    async with AsyncSession(
        async_engine, expire_on_commit=False, autoflush=False
    ) as session:
        notion_repository = NotionRepository(session)
        notion_service = SyncNotionService(notion_repository)
        notion_client = Client(auth=access_token)
        all_search_result = fetch_notion_pages(notion_client)
        await store_notion_pages(all_search_result, notion_service, user_id)


celery.conf.beat_schedule = {
    "ping_telemetry": {
        "task": f"{__name__}.ping_telemetry",
        "schedule": crontab(minute="*/30", hour="*"),
    },
    "process_active_syncs_task": {
        "task": "process_active_syncs_task",
        "schedule": crontab(minute="*/1", hour="*"),
    },
    "process_premium_users": {
        "task": "check_is_premium_task",
        "schedule": crontab(minute="*/1", hour="*"),
    },
    "process_notion_sync": {
        "task": "process_notion_sync",
        "schedule": crontab(minute="0", hour="*/6"),
    },
}
