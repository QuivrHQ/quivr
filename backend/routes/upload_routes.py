import os
from typing import Optional
from uuid import UUID

from celery_worker import process_file_and_notify
from fastapi import APIRouter, Depends, HTTPException, Query, Request, UploadFile
from logger import get_logger
from middlewares.auth import AuthBearer, get_current_user
from models import UserUsage
from models.databases.supabase.knowledge import CreateKnowledgeProperties
from models.databases.supabase.notifications import CreateNotificationProperties
from models.notifications import NotificationsStatusEnum
from modules.user.entity.user_identity import UserIdentity
from packages.files.file import convert_bytes, get_file_size
from repository.knowledge.add_knowledge import add_knowledge
from repository.files.upload_file import upload_file_storage
from repository.notification.add_notification import add_notification

from routes.authorizations.brain_authorization import (
    RoleEnum,
    validate_brain_authorization,
)

logger = get_logger(__name__)
upload_router = APIRouter()


@upload_router.get("/upload/healthz", tags=["Health"])
async def healthz():
    return {"status": "ok"}


@upload_router.post("/upload", dependencies=[Depends(AuthBearer())], tags=["Upload"])
async def upload_file(
    request: Request,
    uploadFile: UploadFile,
    brain_id: UUID = Query(..., description="The ID of the brain"),
    chat_id: Optional[UUID] = Query(None, description="The ID of the chat"),
    current_user: UserIdentity = Depends(get_current_user),
):
    validate_brain_authorization(
        brain_id, current_user.id, [RoleEnum.Editor, RoleEnum.Owner]
    )

    user_daily_usage = UserUsage(
        id=current_user.id,
        email=current_user.email,
    )

    user_settings = user_daily_usage.get_user_settings()

    remaining_free_space = user_settings.get("max_brain_size", 1000000000)

    file_size = get_file_size(uploadFile)
    if remaining_free_space - file_size < 0:
        message = f"Brain will exceed maximum capacity. Maximum file allowed is : {convert_bytes(remaining_free_space)}"
        raise HTTPException(status_code=403, detail=message)
    upload_notification = None
    if chat_id:
        upload_notification = add_notification(
            CreateNotificationProperties(
                action="UPLOAD",
                chat_id=chat_id,
                status=NotificationsStatusEnum.Pending,
            )
        )

    file_content = await uploadFile.read()
    filename_with_brain_id = str(brain_id) + "/" + str(uploadFile.filename)

    try:
        file_in_storage = upload_file_storage(file_content, filename_with_brain_id)
        logger.info(f"File {file_in_storage} uploaded successfully")

    except Exception as e:
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

    added_knowledge = add_knowledge(knowledge_to_add)
    logger.info(f"Knowledge {added_knowledge} added successfully")

    process_file_and_notify.delay(
        file_name=filename_with_brain_id,
        file_original_name=uploadFile.filename,
        brain_id=brain_id,
        notification_id=upload_notification.id if upload_notification else None,
    )
    return {"message": "File processing has started."}
