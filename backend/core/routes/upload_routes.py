import os
from uuid import UUID

from auth import AuthBearer, get_current_user
from fastapi import APIRouter, Depends, Query, Request, UploadFile
from models.brains import Brain
from models.files import File
from models.settings import common_dependencies
from models.users import User
from utils.file import convert_bytes, get_file_size
from utils.processors import filter_file

from routes.authorizations.brain_authorization import (
    RoleEnum,
    validate_brain_authorization,
)

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
    commons = common_dependencies()

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
        message = await filter_file(
            commons,
            file,
            enable_summarization,
            brain_id=brain_id,
            openai_api_key=request.headers.get("Openai-Api-Key", None),
        )

    return message
