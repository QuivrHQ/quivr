import os
from typing import Optional
from uuid import UUID

from celery_worker import process_file_and_notify
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile
from logger import get_logger
from middlewares.auth import AuthBearer, get_current_user
from modules.brain.entity.brain_entity import RoleEnum
from modules.brain.service.brain_authorization_service import (
    validate_brain_authorization,
)
from modules.knowledge.dto.inputs import CreateKnowledgeProperties
from modules.knowledge.service.knowledge_service import KnowledgeService
from modules.notification.dto.inputs import (
    CreateNotification,
    NotificationUpdatableProperties,
)
from modules.notification.entity.notification import NotificationsStatusEnum
from modules.notification.service.notification_service import NotificationService
from modules.upload.service.upload_file import upload_file_storage
from modules.user.entity.user_identity import UserIdentity
from modules.user.service.user_usage import UserUsage
from packages.files.file import convert_bytes, get_file_size
from packages.utils.telemetry import maybe_send_telemetry

logger = get_logger(__name__)
upload_router = APIRouter()

notification_service = NotificationService()
knowledge_service = KnowledgeService()


@upload_router.get("/upload/healthz", tags=["Health"])
async def healthz():
    return {"status": "ok"}


@upload_router.post("/upload", dependencies=[Depends(AuthBearer())], tags=["Upload"])
async def upload_file(
    uploadFile: UploadFile,
    brain_id: UUID = Query(..., description="The ID of the brain"),
    chat_id: Optional[UUID] = Query(None, description="The ID of the chat"),
    current_user: UserIdentity = Depends(get_current_user),
):
    validate_brain_authorization(
        brain_id, current_user.id, [RoleEnum.Editor, RoleEnum.Owner]
    )
    uploadFile.file.seek(0)
    user_daily_usage = UserUsage(
        id=current_user.id,
        email=current_user.email,
    )

    upload_notification = notification_service.add_notification(
        CreateNotification(
            user_id=current_user.id,
            status=NotificationsStatusEnum.INFO,
            title=f"Processing File {uploadFile.filename}",
        )
    )

    user_settings = user_daily_usage.get_user_settings()

    remaining_free_space = user_settings.get("max_brain_size", 1000000000)
    maybe_send_telemetry("upload_file", {"file_name": uploadFile.filename})
    file_size = get_file_size(uploadFile)
    if remaining_free_space - file_size < 0:
        message = f"Brain will exceed maximum capacity. Maximum file allowed is : {convert_bytes(remaining_free_space)}"
        raise HTTPException(status_code=403, detail=message)

    file_content = await uploadFile.read()

    filename_with_brain_id = str(brain_id) + "/" + str(uploadFile.filename)

    try:
        upload_file_storage(file_content, filename_with_brain_id)

    except Exception as e:
        print(e)

        notification_service.update_notification_by_id(
            upload_notification.id if upload_notification else None,
            NotificationUpdatableProperties(
                status=NotificationsStatusEnum.ERROR,
                description=f"There was an error uploading the file: {e}",
            ),
        )
        if "The resource already exists" in str(e):
            raise HTTPException(
                status_code=403,
                detail=f"File {uploadFile.filename} already exists in storage.",
            )
        else:
            raise HTTPException(
                status_code=500, detail=f"Failed to upload file to storage. {e}"
            )

    knowledge_to_add = CreateKnowledgeProperties(
        brain_id=brain_id,
        file_name=uploadFile.filename,
        extension=os.path.splitext(
            uploadFile.filename  # pyright: ignore reportPrivateUsage=none
        )[-1].lower(),
    )

    knowledge_service.add_knowledge(knowledge_to_add)

    process_file_and_notify.delay(
        file_name=filename_with_brain_id,
        file_original_name=uploadFile.filename,
        brain_id=brain_id,
        notification_id=upload_notification.id,
    )
    return {"message": "File processing has started."}
