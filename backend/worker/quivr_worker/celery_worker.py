import asyncio
import os
from uuid import UUID

from celery.exceptions import SoftTimeLimitExceeded, TimeLimitExceeded
from celery.schedules import crontab
from celery.signals import worker_process_init
from dotenv import load_dotenv
from quivr_api.celery_config import celery
from quivr_api.logger import get_logger
from quivr_api.models.settings import settings
from quivr_api.modules.brain.integrations.Notion.Notion_connector import NotionConnector
from quivr_api.modules.dependencies import get_supabase_client
from quivr_api.utils.telemetry import maybe_send_telemetry
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from quivr_worker.assistants.assistants import aprocess_assistant_task
from quivr_worker.check_premium import check_is_premium
from quivr_worker.process import aprocess_file_task
from quivr_worker.syncs.update_syncs import refresh_sync_files, refresh_sync_folders
from quivr_worker.utils.utils import _patch_json

load_dotenv()

get_logger("quivr_core")
logger = get_logger("celery_worker")
_patch_json()

supabase_client = get_supabase_client()
async_engine: AsyncEngine | None = None


@worker_process_init.connect
def init_worker(**kwargs):
    global async_engine
    if not async_engine:
        async_engine = create_async_engine(
            settings.pg_database_async_url,
            connect_args={
                "server_settings": {"application_name": f"quivr-worker-{os.getpid()}"}
            },
            echo=True if os.getenv("ORM_DEBUG") else False,
            future=True,
            # NOTE: pessimistic bound on reconnect
            pool_pre_ping=True,
            # NOTE: no bouncer for now
            pool_size=1,
            pool_recycle=1800,
        )


@celery.task(
    retries=3,
    default_retry_delay=1,
    name="process_file_task",
    time_limit=600,  # 10 min
    soft_time_limit=300,
    autoretry_for=(Exception,),  # SoftTimeLimitExceeded  should not included?
    dont_autoretry_for=(SoftTimeLimitExceeded, TimeLimitExceeded),
)
def process_file_task(
    knowledge_id: UUID,
    notification_id: UUID | None = None,
):
    if async_engine is None:
        init_worker()
    assert async_engine
    logger.info(
        f"Task process_file started for knowledge_id={knowledge_id}, notification_id={notification_id}"
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        aprocess_file_task(async_engine=async_engine, knowledge_id=knowledge_id)
    )


@celery.task(
    retries=3,
    default_retry_delay=1,
    name="refresh_sync_files_task",
    soft_time_limit=3600,
    autoretry_for=(Exception,),
)
def refresh_sync_files_task():
    if async_engine is None:
        init_worker()
    assert async_engine
    logger.info("Update sync task started")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(refresh_sync_files(async_engine=async_engine))


@celery.task(
    retries=3,
    default_retry_delay=1,
    name="refresh_sync_folders_task",
    autoretry_for=(Exception,),
)
def refresh_sync_folders_task():
    if async_engine is None:
        init_worker()
    assert async_engine
    logger.info("Update sync task started")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(refresh_sync_folders(async_engine=async_engine))


@celery.task(
    retries=3,
    default_retry_delay=1,
    name="process_assistant_task",
    autoretry_for=(Exception,),
)
def process_assistant_task(
    assistant_id: str,
    notification_uuid: str,
    task_id: int,
    user_id: str,
):
    if async_engine is None:
        init_worker()
    assert async_engine
    logger.info(
        f"process_assistant_task started for assistant_id={assistant_id}, notification_uuid={notification_uuid}, task_id={task_id}"
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        aprocess_assistant_task(
            async_engine,
            assistant_id,
            notification_uuid,
            task_id,
            user_id,
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


celery.conf.beat_schedule = {
    "ping_telemetry": {
        "task": f"{__name__}.ping_telemetry",
        "schedule": crontab(minute="*/30", hour="*"),
    },
    "process_premium_users": {
        "task": "check_is_premium_task",
        "schedule": crontab(minute="*/1", hour="*"),
    },
    "refresh_sync_files": {
        "task": "refresh_sync_files_task",
        "schedule": crontab(hour="*/8"),
    },
    "refresh_sync_folders": {
        "task": "refresh_sync_folders_task",
        "schedule": crontab(hour="*/8"),
    },
}
