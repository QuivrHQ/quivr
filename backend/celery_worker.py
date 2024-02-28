import asyncio
import io
import os
from datetime import datetime, timedelta, timezone

from celery.schedules import crontab
from celery_config import celery
from fastapi import UploadFile
from logger import get_logger
from models.files import File
from models.settings import get_supabase_client
from modules.brain.integrations.Notion.Notion_connector import NotionConnector
from modules.brain.repository.integration_brains import IntegrationBrain
from modules.brain.service.brain_service import BrainService
from modules.brain.service.brain_vector_service import BrainVectorService
from modules.notification.dto.inputs import NotificationUpdatableProperties
from modules.notification.entity.notification import NotificationsStatusEnum
from modules.notification.service.notification_service import NotificationService
from modules.onboarding.service.onboarding_service import OnboardingService
from packages.files.crawl.crawler import CrawlWebsite
from packages.files.parsers.github import process_github
from packages.files.processors import filter_file

logger = get_logger(__name__)

onboardingService = OnboardingService()
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
            brain_vector_service = BrainVectorService(brain_id)
            if delete_file:  # TODO fix bug
                brain_vector_service.delete_file_from_brain(
                    file_original_name, only_vectors=True
                )
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
                notification_service.update_notification_by_id(
                    notification_id,
                    NotificationUpdatableProperties(
                        status=NotificationsStatusEnum.Done,
                        message=str(notification_message),
                    ),
                )
            brain_service.update_brain_last_update_time(brain_id)

            return True
    except TimeoutError:
        logger.error("TimeoutError")

    except Exception as e:
        notification_message = {
            "status": "error",
            "message": "There was an error uploading the file. Please check the file and try again. If the issue persist, please open an issue on Github",
            "name": file_instance.file.filename if file_instance.file else "",
        }
        notification_service.update_notification_by_id(
            notification_id,
            NotificationUpdatableProperties(
                status=NotificationsStatusEnum.Done,
                message=str(notification_message),
            ),
        )
        raise e


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
        notification_service.update_notification_by_id(
            notification_id,
            NotificationUpdatableProperties(
                status=NotificationsStatusEnum.Done,
                message=str(notification_message),
            ),
        )
    brain_service.update_brain_last_update_time(brain_id)
    return True


@celery.task
def remove_onboarding_more_than_x_days_task():
    onboardingService.remove_onboarding_more_than_x_days(7)


@celery.task(name="NotionConnectorLoad")
def process_integration_brain_created_initial_load(brain_id, user_id):
    notion_connector = NotionConnector(brain_id=brain_id, user_id=user_id)

    pages = notion_connector.load()

    print("pages: ", len(pages))


@celery.task
def process_integration_brain_sync_user_brain(brain_id, user_id):
    notion_connector = NotionConnector(brain_id=brain_id, user_id=user_id)

    notion_connector.poll()


@celery.task
def process_integration_brain_sync():
    integration = IntegrationBrain()
    integrations = integration.get_integration_brain_by_type_integration("notion")

    time = datetime.now(timezone.utc)  # Make `time` timezone-aware
    # last_synced is a string that represents a timestampz in the database
    # only call process_integration_brain_sync_user_brain if more than 1 day has passed since the last sync
    for integration in integrations:
        print(f"last_synced: {integration.last_synced}")  # Add this line
        last_synced = datetime.strptime(
            integration.last_synced, "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        if last_synced < time - timedelta(hours=12):
            process_integration_brain_sync_user_brain.delay(
                brain_id=integration.brain_id, user_id=integration.user_id
            )


celery.conf.beat_schedule = {
    "remove_onboarding_more_than_x_days_task": {
        "task": f"{__name__}.remove_onboarding_more_than_x_days_task",
        "schedule": crontab(minute="0", hour="0"),
    },
    "process_integration_brain_sync": {
        "task": f"{__name__}.process_integration_brain_sync",
        "schedule": crontab(minute="*/5", hour="*"),
    },
}
