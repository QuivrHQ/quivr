import asyncio
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from uuid import UUID

from celery.schedules import crontab
from dotenv import load_dotenv
from quivr_api.celery_config import celery
from quivr_api.logger import get_logger
from quivr_api.models.settings import get_supabase_client
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
from worker.quivr_worker.check_premium import check_is_premium

from quivr_worker.crawl.crawler import CrawlWebsite, slugify
from quivr_worker.files import File
from quivr_worker.processors import process_file
from quivr_worker.syncs.process_active_syncs import process_all_syncs

load_dotenv()

logger = get_logger("celery_worker")

# FIXME: load at init time
# Services
supabase_client = get_supabase_client()
notification_service = NotificationService()
brain_service = BrainService()
sync_active_service = SyncService()
sync_user_service = SyncUserService()
sync_files_repo_service = SyncFiles()
storage = Storage()


@celery.task(
    retries=3,
    default_retry_delay=1,
    name="process_file_and_notify",
    autoretry_for=(Exception,),
)
async def process_file_and_notify(
    file_name: str,
    file_original_name: str,
    brain_id: UUID,
    notification_id: UUID,
    knowledge_id: UUID,
    integration: str | None = None,
    integration_link: str | None = None,
    delete_file: bool = False,
):

    brain = brain_service.get_brain_by_id(brain_id)
    if brain is None:
        logger.exception(
            "It seems like you're uploading knowledge to an unknown brain."
        )
        return
    logger.debug(
        f"process_file started for file_name={file_name}, knowledge_id={knowledge_id}, brain_id={brain_id}, notification_id={notification_id}"
    )

    tmp_name = file_name.replace("/", "_")
    base_file_name = os.path.basename(file_name)
    _, file_extension = os.path.splitext(base_file_name)

    brain_vector_service = BrainVectorService(brain_id)

    # FIXME: @chloedia @AmineDiro
    # We should decide if these checks should happen at API level or Worker level
    # These checks should use Knowledge table (where we should store knowledge sha1)
    # file_exists = file_already_exists()
    # file_exists_in_brain = file_already_exists_in_brain(brain.brain_id)

    with NamedTemporaryFile(
        suffix="_" + tmp_name,  # pyright: ignore reportPrivateUsage=none
    ) as tmp_file:
        # This reads the whole file to memory
        file_data = supabase_client.storage.from_("quivr").download(file_name)
        tmp_file.write(file_data)
        tmp_file.flush()
        file_instance = File(
            file_name=base_file_name,
            tmp_file_path=Path(tmp_file.name),
            bytes_content=file_data,
            file_size=len(file_data),
            file_extension=file_extension,
        )

        if delete_file:  # TODO fix bug
            brain_vector_service.delete_file_from_brain(
                file_original_name, only_vectors=True
            )

        await process_file(
            file=file_instance,
            brain=brain,
            integration=integration,
            integration_link=integration_link,
        )

        brain_service.update_brain_last_update_time(brain_id)


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
            file_name=file_name,
            tmp_file_path=Path(tmp_file.name),
            bytes_content=extracted_content_bytes,
            file_size=len(extracted_content),
            file_extension=".txt",
        )
        # TODO(@aminediro): call process website function
        await process_file(
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
