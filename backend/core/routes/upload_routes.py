import os
from uuid import UUID

from auth import AuthBearer, get_current_user
from fastapi import APIRouter, Depends, Query, Request, UploadFile
from models.brains import Brain
from models.files import File
from models.users import User
from repository.brain.get_brain_details import get_brain_details
from repository.user_identity.get_user_identity import get_user_identity
from routes.authorizations.brain_authorization import (
    RoleEnum,
    validate_brain_authorization,
)
from utils.file import convert_bytes, get_file_size
from utils.processors import filter_file

upload_router = APIRouter()


@upload_router.post("/upload", dependencies=[Depends(AuthBearer())], tags=["Upload"])
async def upload_file(
    request: Request,
    uploadFile: UploadFile,
    brain_id: UUID = Query(..., description="The ID of the brain"),
    enable_summarization: bool = False,
    current_user: User = Depends(get_current_user),
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

    if request.headers.get("Openai-Api-Key"):
        brain.max_brain_size = int(os.getenv("MAX_BRAIN_SIZE_WITH_KEY", 209715200))

    remaining_free_space = brain.remaining_brain_size

    file_size = get_file_size(uploadFile)

    file = File(file=uploadFile)
    if remaining_free_space - file_size < 0:
        message = {
            "message": f"❌ User's brain will exceed maximum capacity with this upload. Maximum file allowed is : {convert_bytes(remaining_free_space)}",
            "type": "error",
        }
    else:
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

    return message
