import os
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, UploadFile
from quivr_api.celery_worker import process_file_and_notify
from quivr_api.logger import get_logger
from quivr_api.modules.brain.entity.brain_entity import RoleEnum
from quivr_api.modules.brain.service.brain_authorization_service import (
    validate_brain_authorization,
)
from quivr_api.modules.knowledge.dto.inputs import CreateKnowledgeProperties
from quivr_api.modules.knowledge.service.knowledge_service import KnowledgeService
from quivr_api.modules.notification.dto.inputs import NotificationUpdatableProperties
from quivr_api.modules.notification.entity.notification import NotificationsStatusEnum
from quivr_api.modules.notification.service.notification_service import (
    NotificationService,
)
from quivr_api.modules.upload.service.upload_file import upload_file_storage
from quivr_api.modules.user.service.user_usage import UserUsage
from quivr_api.packages.files.file import convert_bytes, get_file_size
from quivr_api.packages.utils.telemetry import maybe_send_telemetry

logger = get_logger("upload_file")

knowledge_service = KnowledgeService()
notification_service = NotificationService()


async def upload_file(
    upload_file: UploadFile,
    brain_id: UUID,
    current_user: str,
    bulk_id: Optional[UUID] = None,
    integration: Optional[str] = None,
    integration_link: Optional[str] = None,
    notification_id: Optional[UUID] = None,
):
    validate_brain_authorization(
        brain_id, current_user, [RoleEnum.Editor, RoleEnum.Owner]
    )
    user_daily_usage = UserUsage(
        id=current_user,
    )

    user_settings = user_daily_usage.get_user_settings()

    remaining_free_space = user_settings.get("max_brain_size", 1000000000)
    maybe_send_telemetry("upload_file", {"file_name": upload_file.filename})
    file_size = get_file_size(upload_file)
    if remaining_free_space - file_size < 0:
        message = f"Brain will exceed maximum capacity. Maximum file allowed is : {convert_bytes(remaining_free_space)}"
        raise HTTPException(status_code=403, detail=message)

    file_content = await upload_file.read()

    filename_with_brain_id = str(brain_id) + "/" + str(upload_file.filename)

    try:
        file_in_storage = upload_file_storage(file_content, filename_with_brain_id)

    except Exception as e:
        print(e)

        if "The resource already exists" in str(e):
            notification_service.update_notification_by_id(
                notification_id,
                NotificationUpdatableProperties(
                    status=NotificationsStatusEnum.ERROR,
                    description=f"File {upload_file.filename} already exists in storage.",
                ),
            )
            raise HTTPException(
                status_code=403,
                detail=f"File {upload_file.filename} already exists in storage.",
            )
        
        else:
            notification_service.update_notification_by_id(
                notification_id,
                NotificationUpdatableProperties(
                    status=NotificationsStatusEnum.ERROR,
                    description=f"There was an error uploading the file",
                ),
            )
            raise HTTPException(
                status_code=500, detail=f"Failed to upload file to storage. {e}"
            )

    knowledge_to_add = CreateKnowledgeProperties(
        brain_id=brain_id,
        file_name=upload_file.filename,
        extension=os.path.splitext(
            upload_file.filename  # pyright: ignore reportPrivateUsage=none
        )[-1].lower(),
        integration=integration,
        integration_link=integration_link,
    )

    added_knowledge = knowledge_service.add_knowledge(knowledge_to_add)

    process_file_and_notify.delay(
        file_name=filename_with_brain_id,
        file_original_name=upload_file.filename,
        integration=integration,
        integration_link=integration_link,
        brain_id=brain_id,
        notification_id=notification_id,
        knowledge_id=added_knowledge.id,
    )
    return {"message": "File processing has started."}
