import os
from tempfile import NamedTemporaryFile
from uuid import UUID

from celery.schedules import crontab

from quivr_core.api.celery_config import celery
from quivr_core.api.logger import get_logger
from quivr_core.api.models.files import File
from quivr_core.api.models.settings import get_supabase_client
from quivr_core.api.modules.brain.service.brain_service import BrainService
from quivr_core.api.modules.brain.service.brain_vector_service import BrainVectorService
from quivr_core.api.modules.notification.dto.inputs import (
    NotificationUpdatableProperties,
)
from quivr_core.api.modules.notification.entity.notification import (
    NotificationsStatusEnum,
)
from quivr_core.api.modules.notification.service.notification_service import (
    NotificationService,
)
from quivr_core.api.packages.files.crawl.crawler import CrawlWebsite, slugify
from quivr_core.api.packages.files.parsers.github import process_github
from quivr_core.api.packages.files.processors import filter_file
from quivr_core.api.packages.utils.telemetry import maybe_send_telemetry

logger = get_logger(__name__)

notification_service = NotificationService()
brain_service = BrainService()


@celery.task(name="process_file_and_notify")
def process_file_and_notify(
    file_name: str,
    file_original_name: str,
    brain_id,
    notification_id=None,
    integration=None,
    delete_file=False,
):
    try:
        supabase_client = get_supabase_client()
        tmp_name = file_name.replace("/", "_")
        base_file_name = os.path.basename(file_name)
        _, file_extension = os.path.splitext(base_file_name)

        with NamedTemporaryFile(
            suffix="_" + tmp_name,  # pyright: ignore reportPrivateUsage=none
        ) as tmp_file:
            res = supabase_client.storage.from_("quivr").download(file_name)
            tmp_file.write(res)
            tmp_file.flush()
            file_instance = File(
                file_name=base_file_name,
                tmp_file_path=tmp_file.name,
                bytes_content=res,
                file_size=len(res),
                file_extension=file_extension,
            )
            brain_vector_service = BrainVectorService(brain_id)
            if delete_file:  # TODO fix bug
                brain_vector_service.delete_file_from_brain(
                    file_original_name, only_vectors=True
                )

            filter_file(
                file=file_instance,
                brain_id=brain_id,
                original_file_name=file_original_name,
            )

            if notification_id:
                notification_service.update_notification_by_id(
                    notification_id,
                    NotificationUpdatableProperties(
                        status=NotificationsStatusEnum.SUCCESS,
                        description="Your file has been properly uploaded!",
                    ),
                )
            brain_service.update_brain_last_update_time(brain_id)

            return True

    except TimeoutError:
        logger.error("TimeoutError")

    except Exception as e:
        logger.exception(e)
        notification_service.update_notification_by_id(
            notification_id,
            NotificationUpdatableProperties(
                status=NotificationsStatusEnum.ERROR,
                description=f"An error occurred while processing the file: {e}",
            ),
        )


@celery.task(name="process_crawl_and_notify")
def process_crawl_and_notify(
    crawl_website_url: str,
    brain_id: UUID,
    notification_id=None,
):
    crawl_website = CrawlWebsite(url=crawl_website_url)

    if not crawl_website.checkGithub():
        # Build file data
        extracted_content = crawl_website.process()
        extracted_content_bytes = extracted_content.encode("utf-8")
        file_name = slugify(crawl_website.url) + ".txt"

        with NamedTemporaryFile(
            suffix="_" + file_name,  # pyright: ignore reportPrivateUsage=none
        ) as tmp_file:
            tmp_file.write(extracted_content_bytes)
            tmp_file.flush()
            file_instance = File(
                file_name=file_name,
                tmp_file_path=tmp_file.name,
                bytes_content=extracted_content_bytes,
                file_size=len(extracted_content),
                file_extension=".txt",
            )
            filter_file(
                file=file_instance,
                brain_id=brain_id,
                original_file_name=crawl_website_url,
            )
            notification_service.update_notification_by_id(
                notification_id,
                NotificationUpdatableProperties(
                    status=NotificationsStatusEnum.SUCCESS,
                    description="Your URL has been properly crawled!",
                ),
            )
    else:
        process_github(
            repo=crawl_website.url,
            brain_id=brain_id,
        )

    if notification_id:
        notification_service.update_notification_by_id(
            notification_id,
            NotificationUpdatableProperties(
                status=NotificationsStatusEnum.SUCCESS,
                description="Your file has been properly uploaded!",
            ),
        )

    brain_service.update_brain_last_update_time(brain_id)
    return True


@celery.task
def ping_telemetry():
    maybe_send_telemetry("ping", {"ping": "pong"})


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
        "task": "check_if_is_premium_user",
        "schedule": crontab(minute="*/1", hour="*"),
    },
}
