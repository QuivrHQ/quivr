import asyncio
from pathlib import Path
from tempfile import NamedTemporaryFile
from uuid import UUID

from celery.schedules import crontab
from dotenv import load_dotenv
from quivr_api.celery_config import celery
from quivr_api.logger import get_logger
from quivr_api.models.settings import get_documents_vector_store, get_supabase_client
from quivr_api.modules.brain.integrations.Notion.Notion_connector import NotionConnector
from quivr_api.modules.brain.service.brain_service import BrainService
from quivr_api.modules.brain.service.brain_vector_service import BrainVectorService
from quivr_api.modules.knowledge.repository.storage import Storage
from quivr_api.modules.notification.service.notification_service import (
    NotificationService,
)
from quivr_api.modules.sync.repository.sync_files import SyncFiles
from quivr_api.modules.sync.service.sync_service import SyncService, SyncUserService
from quivr_api.utils.telemetry import maybe_send_telemetry

from quivr_worker.check_premium import check_is_premium
from quivr_worker.crawl.crawler import CrawlWebsite, slugify
from quivr_worker.files import File, compute_sha1
from quivr_worker.process.process_file import parse_file, process_file_func
from quivr_worker.syncs.process_active_syncs import process_all_syncs

load_dotenv()

logger = get_logger("celery_worker")

# FIXME: load at init time
# Services
supabase_client = get_supabase_client()
document_vector_store = get_documents_vector_store()
notification_service = NotificationService()
brain_service = BrainService()
sync_active_service = SyncService()
sync_user_service = SyncUserService()
sync_files_repo_service = SyncFiles()
storage = Storage()


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
        process_file_func(
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
async def process_crawl_and_notify(
    crawl_website_url: str,
    brain_id: UUID,
    knowledge_id: UUID,
    notification_id: UUID | None = None,
):
    crawl_website = CrawlWebsite(url=crawl_website_url)

    # Build file data
    extracted_content = crawl_website.process()
    extracted_content_bytes = extracted_content.encode("utf-8")
    file_name = slugify(crawl_website.url) + ".txt"

    brain = brain_service.get_brain_by_id(brain_id)
    if brain is None:
        logger.exception(
            "It seems like you're uploading knowledge to an unknown brain."
        )
        return

    with NamedTemporaryFile(
        suffix="_" + file_name,  # pyright: ignore reportPrivateUsage=none
    ) as tmp_file:
        tmp_file.write(extracted_content_bytes)
        tmp_file.flush()
        file_instance = File(
            knowledge_id=knowledge_id,
            file_name=file_name,
            tmp_file_path=Path(tmp_file.name),
            file_size=len(extracted_content),
            file_extension=".txt",
            file_sha1=compute_sha1(extracted_content_bytes),
        )
        # TODO(@aminediro): call process website function
        await parse_file(
            file=file_instance,
            brain=brain,
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


@celery.task(name="process_sync_active")
def process_sync_active():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        process_all_syncs(
            sync_active_service, sync_user_service, sync_files_repo_service, storage
        )
    )


celery.conf.beat_schedule = {
    "ping_telemetry": {
        "task": f"{__name__}.ping_telemetry",
        "schedule": crontab(minute="*/30", hour="*"),
    },
    "process_sync_active": {
        "task": "process_sync_active",
        "schedule": crontab(minute="*/1", hour="*"),
    },
    "process_premium_users": {
        "task": "check_is_premium_task",
        "schedule": crontab(minute="*/1", hour="*"),
    },
}
