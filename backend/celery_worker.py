import asyncio
import io
import os

from celery import Celery
from celery.schedules import crontab
from fastapi import UploadFile
from models.databases.supabase.notifications import NotificationUpdatableProperties
from models.files import File
from models.notifications import NotificationsStatusEnum
from models.settings import get_supabase_client
from modules.onboarding.service.onboarding_service import OnboardingService
from packages.files.crawl.crawler import CrawlWebsite
from packages.files.parsers.github import process_github
from packages.files.processors import filter_file
from repository.brain.update_brain_last_update_time import update_brain_last_update_time
from repository.notification.update_notification import update_notification_by_id

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "")
CELEBRY_BROKER_QUEUE_NAME = os.getenv("CELEBRY_BROKER_QUEUE_NAME", "quivr")

onboardingService = OnboardingService()

if CELERY_BROKER_URL.startswith("sqs"):
    broker_transport_options = {
        CELEBRY_BROKER_QUEUE_NAME: {
            "my-q": {
                "url": CELERY_BROKER_URL,
            }
        }
    }
    celery = Celery(
        __name__,
        broker=CELERY_BROKER_URL,
        task_serializer="json",
        task_concurrency=4,
        worker_prefetch_multiplier=1,
        broker_transport_options=broker_transport_options,
    )
    celery.conf.task_default_queue = CELEBRY_BROKER_QUEUE_NAME
elif CELERY_BROKER_URL.startswith("redis"):
    celery = Celery(
        __name__,
        broker=CELERY_BROKER_URL,
        backend=CELERY_BROKER_URL,
        task_concurrency=4,
        worker_prefetch_multiplier=1,
        task_serializer="json",
    )
else:
    raise ValueError(f"Unsupported broker URL: {CELERY_BROKER_URL}")


@celery.task(name="process_file_and_notify")
def process_file_and_notify(
    file_name: str,
    file_original_name: str,
    brain_id,
    notification_id=None,
):
    supabase_client = get_supabase_client()
    tmp_file_name = "tmp-file-" + file_name
    tmp_file_name = tmp_file_name.replace("/", "_")

    with open(tmp_file_name, "wb+") as f:
        res = supabase_client.storage.from_("quivr").download(file_name)
        f.write(res)
        f.seek(0)
        file_content = f.read()

        upload_file = UploadFile(
            file=f, filename=file_name.split("/")[-1], size=len(file_content)
        )

        file_instance = File(file=upload_file)
        loop = asyncio.get_event_loop()
        message = loop.run_until_complete(
            filter_file(
                file=file_instance,
                brain_id=brain_id,
                original_file_name=file_original_name,
            )
        )

        f.close()
        os.remove(tmp_file_name)

        if notification_id:
            notification_message = {
                "status": message["type"],
                "message": message["message"],
                "name": file_instance.file.filename if file_instance.file else "",
            }
            update_notification_by_id(
                notification_id,
                NotificationUpdatableProperties(
                    status=NotificationsStatusEnum.Done,
                    message=str(notification_message),
                ),
            )
        update_brain_last_update_time(brain_id)

        return True


@celery.task(name="process_crawl_and_notify")
def process_crawl_and_notify(
    crawl_website_url,
    brain_id,
    notification_id=None,
):
    crawl_website = CrawlWebsite(url=crawl_website_url)

    if not crawl_website.checkGithub():
        file_path, file_name = crawl_website.process()

        with open(file_path, "rb") as f:
            file_content = f.read()

        # Create a file-like object in memory using BytesIO
        file_object = io.BytesIO(file_content)
        upload_file = UploadFile(
            file=file_object, filename=file_name, size=len(file_content)
        )
        file_instance = File(file=upload_file)

        loop = asyncio.get_event_loop()
        message = loop.run_until_complete(
            filter_file(
                file=file_instance,
                brain_id=brain_id,
                original_file_name=crawl_website_url,
            )
        )
    else:
        loop = asyncio.get_event_loop()
        message = loop.run_until_complete(
            process_github(
                repo=crawl_website.url,
                brain_id=brain_id,
            )
        )

    if notification_id:
        notification_message = {
            "status": message["type"],
            "message": message["message"],
            "name": crawl_website_url,
        }
        update_notification_by_id(
            notification_id,
            NotificationUpdatableProperties(
                status=NotificationsStatusEnum.Done,
                message=str(notification_message),
            ),
        )
    update_brain_last_update_time(brain_id)
    return True


@celery.task
def remove_onboarding_more_than_x_days_task():
    onboardingService.remove_onboarding_more_than_x_days(7)


celery.conf.beat_schedule = {
    "remove_onboarding_more_than_x_days_task": {
        "task": f"{__name__}.remove_onboarding_more_than_x_days_task",
        "schedule": crontab(minute="0", hour="0"),
    },
}
