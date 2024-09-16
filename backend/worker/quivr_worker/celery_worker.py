import asyncio
import os
from uuid import UUID

from celery.schedules import crontab
from celery.signals import worker_process_init
from dotenv import load_dotenv
from quivr_api.celery_config import celery
from quivr_api.logger import get_logger
from quivr_api.models.settings import settings
from quivr_api.modules.brain.integrations.Notion.Notion_connector import NotionConnector
from quivr_api.modules.brain.repository.brains_vectors import BrainsVectors
from quivr_api.modules.brain.service.brain_service import BrainService
from quivr_api.modules.dependencies import get_supabase_client
from quivr_api.modules.knowledge.repository.knowledges import KnowledgeRepository
from quivr_api.modules.knowledge.repository.storage import SupabaseS3Storage
from quivr_api.modules.knowledge.service.knowledge_service import KnowledgeService
from quivr_api.modules.notification.service.notification_service import (
    NotificationService,
)
from quivr_api.modules.sync.repository.sync_files import SyncFilesRepository
from quivr_api.modules.sync.service.sync_notion import SyncNotionService
from quivr_api.modules.sync.service.sync_service import SyncService, SyncUserService
from quivr_api.modules.vector.repository.vectors_repository import VectorRepository
from quivr_api.modules.vector.service.vector_service import VectorService
from quivr_api.utils.telemetry import maybe_send_telemetry
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel import Session, text
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_worker.check_premium import check_is_premium
from quivr_worker.process.process_s3_file import process_uploaded_file
from quivr_worker.process.process_url import process_url_func
from quivr_worker.syncs.process_active_syncs import (
    SyncServices,
    process_all_active_syncs,
    process_notion_sync,
    process_sync,
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
sync_active_service = SyncService()
sync_user_service = SyncUserService()
sync_files_repo_service = SyncFilesRepository()
brain_service = BrainService()
brain_vectors = BrainsVectors()
storage = SupabaseS3Storage()
notion_service: SyncNotionService | None = None
async_engine: AsyncEngine | None = None
engine: Engine | None = None


@worker_process_init.connect
def init_worker(**kwargs):
    global async_engine
    global engine
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

    if not engine:
        engine = create_engine(
            settings.pg_database_url,
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
    file_name: str,
    file_original_name: str,
    brain_id: UUID,
    notification_id: UUID,
    knowledge_id: UUID,
    source: str | None = None,
    source_link: str | None = None,
    delete_file: bool = False,
):
    if async_engine is None:
        init_worker()

    logger.info(
        f"Task process_file started for file_name={file_name}, knowledge_id={knowledge_id}, brain_id={brain_id}, notification_id={notification_id}"
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        aprocess_file_task(
            file_name=file_name,
            file_original_name=file_original_name,
            brain_id=brain_id,
            notification_id=notification_id,
            knowledge_id=knowledge_id,
            source=source,
            source_link=source_link,
            delete_file=delete_file,
        )
    )


async def aprocess_file_task(
    file_name: str,
    file_original_name: str,
    brain_id: UUID,
    notification_id: UUID,
    knowledge_id: UUID,
    source: str | None = None,
    source_link: str | None = None,
    delete_file: bool = False,
):
    global engine
    assert engine
    async with AsyncSession(async_engine) as async_session:
        try:
            await async_session.execute(
                text("SET SESSION idle_in_transaction_session_timeout = '5min';")
            )
            with Session(engine, expire_on_commit=False, autoflush=False) as session:
                session.execute(
                    text("SET SESSION idle_in_transaction_session_timeout = '5min';")
                )
                vector_repository = VectorRepository(session)
                vector_service = VectorService(
                    vector_repository
                )  # FIXME @amine: fix to need AsyncSession in vector Service
                knowledge_repository = KnowledgeRepository(async_session)
                knowledge_service = KnowledgeService(knowledge_repository)
                await process_uploaded_file(
                    supabase_client=supabase_client,
                    brain_service=brain_service,
                    vector_service=vector_service,
                    knowledge_service=knowledge_service,
                    file_name=file_name,
                    brain_id=brain_id,
                    file_original_name=file_original_name,
                    knowledge_id=knowledge_id,
                    integration=source,
                    integration_link=source_link,
                    delete_file=delete_file,
                )
                session.commit()
            await async_session.commit()
        except Exception as e:
            session.rollback()
            await async_session.rollback()
            raise e
        finally:
            session.close()
            await async_session.close()


@celery.task(
    retries=3,
    default_retry_delay=1,
    name="process_crawl_task",
    autoretry_for=(Exception,),
)
def process_crawl_task(
    crawl_website_url: str,
    brain_id: UUID,
    knowledge_id: UUID,
    notification_id: UUID | None = None,
):
    logger.info(
        f"Task process_crawl_task started for url={crawl_website_url}, knowledge_id={knowledge_id}, brain_id={brain_id}, notification_id={notification_id}"
    )
    global engine
    assert engine
    try:
        with Session(engine, expire_on_commit=False, autoflush=False) as session:
            session.execute(
                text("SET SESSION idle_in_transaction_session_timeout = '5min';")
            )
            vector_repository = VectorRepository(session)
            vector_service = VectorService(vector_repository)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(
                process_url_func(
                    url=crawl_website_url,
                    brain_id=brain_id,
                    knowledge_id=knowledge_id,
                    brain_service=brain_service,
                    vector_service=vector_service,
                )
            )
            session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


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


@celery.task(name="process_sync_task")
def process_sync_task(
    sync_id: int, user_id: str, files_ids: list[str], folder_ids: list[str]
):
    global async_engine
    assert async_engine
    sync = next(
        filter(lambda s: s.id == sync_id, sync_active_service.get_syncs_active(user_id))
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        process_sync(
            sync=sync,
            files_ids=files_ids,
            folder_ids=folder_ids,
            services=SyncServices(
                async_engine=async_engine,
                sync_active_service=sync_active_service,
                sync_user_service=sync_user_service,
                sync_files_repo_service=sync_files_repo_service,
                storage=storage,
                brain_vectors=brain_vectors,
                notification_service=notification_service,
            ),
        )
    )


@celery.task(name="process_active_syncs_task")
def process_active_syncs_task():
    global async_engine
    assert async_engine
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        process_all_active_syncs(
            SyncServices(
                async_engine=async_engine,
                sync_active_service=sync_active_service,
                sync_user_service=sync_user_service,
                sync_files_repo_service=sync_files_repo_service,
                storage=storage,
                brain_vectors=brain_vectors,
                notification_service=notification_service,
            ),
        )
    )


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


celery.conf.beat_schedule = {
    "ping_telemetry": {
        "task": f"{__name__}.ping_telemetry",
        "schedule": crontab(minute="*/30", hour="*"),
    },
    "process_active_syncs": {
        "task": "process_active_syncs_task",
        "schedule": crontab(minute="*/1", hour="*"),
    },
    "process_premium_users": {
        "task": "check_is_premium_task",
        "schedule": crontab(minute="*/1", hour="*"),
    },
    "process_notion_sync": {
        "task": "process_notion_sync_task",
        "schedule": crontab(minute="0", hour="*/6"),
    },
}
