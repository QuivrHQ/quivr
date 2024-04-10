from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, File, Query, UploadFile
from logger import get_logger
from middlewares.auth import AuthBearer, get_current_user
from modules.assistant.dto.outputs import AssistantOutput
from modules.assistant.ito.audio_transcript import AudioTranscriptAssistant
from modules.assistant.ito.crawler import CrawlerAssistant
from modules.assistant.ito.summary import SummaryAssistant, summary_inputs
from modules.assistant.service.assistant import Assistant
from modules.user.entity.user_identity import UserIdentity

assistant_router = APIRouter()
logger = get_logger(__name__)

assistant_service = Assistant()


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
    return [summary]


@assistant_router.post(
    "/assistant/{ingestion_id}/process",
    dependencies=[Depends(AuthBearer())],
    tags=["Assistant"],
)
async def process_assistant(
    ingestion_id: UUID,
    file_1: UploadFile = File(None),
    current_user: UserIdentity = Depends(get_current_user),
    brain_id: UUID = Query(None, description="The ID of the brain"),
    send_file_email: bool = Query(False, description="Send the file by email"),
    url: str = Query(None, description="The URL to process"),
):
    if ingestion_id is None:
        raise ValueError("Ingestion ID is required")

    assistant = assistant_service.get_assistant_by_id(ingestion_id)

    if assistant.name == "summary":
        summary = SummaryAssistant(
            uploadFile=file_1,
            current_user=current_user,
            brain_id=brain_id,
            send_file_email=send_file_email,
            url=url,
        )
        return await summary.process_assistant()

    if assistant.name == "audio_transcript":
        audio_summary = AudioTranscriptAssistant(
            uploadFile=file_1,
            current_user=current_user,
            brain_id=brain_id,
            send_file_email=send_file_email,
            url=url,
        )
        return await audio_summary.process_assistant()

    if assistant.name == "crawler":
        crawler = CrawlerAssistant(
            uploadFile=file_1,
            current_user=current_user,
            brain_id=brain_id,
            send_file_email=send_file_email,
            url=url,
        )
        return await crawler.process_assistant()

    return {"message": "Not found"}
