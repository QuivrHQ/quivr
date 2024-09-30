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
from quivr_api.modules.dependencies import get_supabase_client
from quivr_api.utils.telemetry import maybe_send_telemetry
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from quivr_worker.assistants.assistants import aprocess_assistant_task
from quivr_worker.check_premium import check_is_premium
from quivr_worker.process import aprocess_file_task
from quivr_worker.syncs.update_syncs import update_sync_files
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
    autoretry_for=(Exception,),
    dont_autoretry_for=(FileExistsError,),
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
    name="process_file_task",
    autoretry_for=(Exception,),
    dont_autoretry_for=(FileExistsError,),
)
def update_sync_task():
    if async_engine is None:
        init_worker()
    assert async_engine
    logger.info("Update sync task started")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_sync_files(async_engine=async_engine))


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


# @celery.task(name="process_notion_sync_task")
# def process_notion_sync_task():
#     global async_engine
#     assert async_engine
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(process_notion_sync(async_engine))


# @celery.task(name="fetch_and_store_notion_files_task")
# def fetch_and_store_notion_files_task(
#     access_token: str, user_id: UUID, sync_user_id: int
# ):
#     if async_engine is None:
#         init_worker()
#     assert async_engine
#     try:
#         logger.debug("Fetching and storing Notion files")
#         loop = asyncio.get_event_loop()
#         loop.run_until_complete(
#             fetch_and_store_notion_files_async(
#                 async_engine, access_token, user_id, sync_user_id
#             )
#         )
#         sync_user_service.update_sync_user_status(
#             sync_user_id=sync_user_id, status=str(SyncStatus.SYNCED)
#         )
#     except Exception:
#         logger.error("Error fetching and storing Notion files")
#         sync_user_service.update_sync_user_status(
#             sync_user_id=sync_user_id, status=str(SyncStatus.ERROR)
#         )


# @celery.task(name="clean_notion_user_syncs")
# def clean_notion_user_syncs():
#     logger.debug("Cleaning Notion user syncs")
#     sync_user_service.clean_notion_user_syncs()


celery.conf.beat_schedule = {
    "ping_telemetry": {
        "task": f"{__name__}.ping_telemetry",
        "schedule": crontab(minute="*/30", hour="*"),
    },
    # "process_active_syncs": {
    #     "task": "process_active_syncs_task",
    #     "schedule": crontab(minute="*/1", hour="*"),
    # },
    "process_premium_users": {
        "task": "check_is_premium_task",
        "schedule": crontab(minute="*/1", hour="*"),
    },
    "process_notion_sync": {
        "task": "process_notion_sync_task",
        "schedule": crontab(minute="0", hour="*/6"),
    },
}
