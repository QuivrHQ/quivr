import asyncio
import base64
import io
import os

from celery import Celery
from fastapi import UploadFile
from models import File
from models.databases.supabase.notifications import NotificationUpdatableProperties
from models.notifications import NotificationsStatusEnum
from repository.notification.update_notification import update_notification_by_id
from utils.processors import filter_file

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)


@celery.task(name="process_file_and_notify")
def process_file_and_notify(
    file,
    file_name,
    enable_summarization,
    brain_id,
    openai_api_key,
    notification_id=None,
):
    print("Processing file")
    file_content = base64.b64decode(file)

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
            enable_summarization=enable_summarization,
            brain_id=brain_id,
            openai_api_key=openai_api_key,
        )
    )

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
    return True
