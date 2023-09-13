from typing import Optional
from uuid import UUID

from auth import AuthBearer, get_current_user
from fastapi import APIRouter, Depends, Query, Request, UploadFile
from models import Brain, File, UserIdentity, UserUsage
from models.databases.supabase.notifications import (
    CreateNotificationProperties,
    NotificationUpdatableProperties,
)
from models.notifications import NotificationsStatusEnum
from repository.brain import get_brain_details
from repository.notification.add_notification import add_notification
from repository.notification.update_notification import update_notification_by_id
from repository.user_identity import get_user_identity
from routes.authorizations.brain_authorization import (
    RoleEnum,
    validate_brain_authorization,
)
from utils.file import convert_bytes, get_file_size
from utils.processors import filter_file

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
    enable_summarization: bool = False,
    current_user: UserIdentity = Depends(get_current_user),
):
    """
    Upload a file to the user's storage.

    - `file`: The file to be uploaded.
    - `enable_summarization`: Flag to enable summarization of the file's content.
    - `current_user`: The current authenticated user.
    - Returns the response message indicating the success or failure of the upload.

    This endpoint allows users to upload files to their storage (brain). It checks the remaining free space in the user's storage (brain)
    and ensures that the file size does not exceed the maximum capacity. If the file is within the allowed size limit,
    it can optionally apply summarization to the file's content. The response message will indicate the status of the upload.
    """
    validate_brain_authorization(
        brain_id, current_user.id, [RoleEnum.Editor, RoleEnum.Owner]
    )

    brain = Brain(id=brain_id)
    userDailyUsage = UserUsage(
        id=current_user.id,
        email=current_user.email,
        openai_api_key=current_user.openai_api_key,
    )
    userSettings = userDailyUsage.get_user_settings()

    if request.headers.get("Openai-Api-Key"):
        brain.max_brain_size = userSettings.get("max_brain_size", 1000000000)

    remaining_free_space = userSettings.get("max_brain_size", 1000000000)

    file_size = get_file_size(uploadFile)

    file = File(file=uploadFile)
    if remaining_free_space - file_size < 0:
        message = {
            "message": f"❌ UserIdentity's brain will exceed maximum capacity with this upload. Maximum file allowed is : {convert_bytes(remaining_free_space)}",
            "type": "error",
        }
    else:
        upload_notification = None
        if chat_id:
            upload_notification = add_notification(
                CreateNotificationProperties(
                    action="UPLOAD",
                    chat_id=chat_id,
                    status=NotificationsStatusEnum.Pending,
                )
            )
        openai_api_key = request.headers.get("Openai-Api-Key", None)
        if openai_api_key is None:
            brain_details = get_brain_details(brain_id)
            if brain_details:
                openai_api_key = brain_details.openai_api_key

        if openai_api_key is None:
            openai_api_key = get_user_identity(current_user.id).openai_api_key

        message = await filter_file(
            file=file,
            enable_summarization=enable_summarization,
            brain_id=brain_id,
            openai_api_key=openai_api_key,
        )
        if not file.file:
            raise Exception("File not found")

        if upload_notification:
            notification_message = {
                "status": message["type"],
                "message": message["message"],
                "name": file.file.filename if file.file else "",
            }
            update_notification_by_id(
                upload_notification.id,
                NotificationUpdatableProperties(
                    status=NotificationsStatusEnum.Done,
                    message=str(notification_message),
                ),
            )

    return message
