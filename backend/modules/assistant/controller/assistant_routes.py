from typing import List

from celery_worker import process_assistant_task
from fastapi import APIRouter, Depends, UploadFile
from logger import get_logger
from middlewares.auth import AuthBearer, get_current_user
from modules.assistant.dto.inputs import InputAssistant
from modules.assistant.dto.outputs import AssistantOutput
from modules.assistant.ito.difference_assistant import difference_inputs
from modules.assistant.ito.summary import summary_inputs
from modules.assistant.service.assistant import Assistant
from modules.notification.service.notification_service import NotificationService
from modules.upload.service.upload_file import upload_file_storage
from modules.user.entity.user_identity import UserIdentity

assistant_router = APIRouter()
logger = get_logger(__name__)

assistant_service = Assistant()
notification_service = NotificationService()


@assistant_router.get(
    "/assistants", dependencies=[Depends(AuthBearer())], tags=["Assistant"]
)
async def list_assistants(
    current_user: UserIdentity = Depends(get_current_user),
) -> List[AssistantOutput]:
    """
    Retrieve and list all the knowledge in a brain.
    """

    summary = summary_inputs()
    difference = difference_inputs()
    # crawler = crawler_inputs()
    # audio_transcript = audio_transcript_inputs()
    return [summary, difference]


@assistant_router.post(
    "/assistant/process",
    dependencies=[Depends(AuthBearer())],
    tags=["Assistant"],
)
async def process_assistant(
    input: InputAssistant,
    files: List[UploadFile] = None,  # type: ignore
    current_user: UserIdentity = Depends(get_current_user),
):
    files_names = []
    for file in files:
        file_content = await file.read()
        upload_file_storage(file_content, str(file.filename), upsert="true")
        files_names.append(file.filename)

    process_assistant_task.delay(
        input_in=input.model_dump_json(),
        files_name=files_names,
        current_user=current_user.model_dump(),
    )
    return {"message": "Assistant is working in the back"}
