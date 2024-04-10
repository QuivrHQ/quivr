from typing import List

from fastapi import APIRouter, Depends, File, UploadFile
from logger import get_logger
from middlewares.auth import AuthBearer, get_current_user
from modules.assistant.dto.inputs import InputAssistant
from modules.assistant.dto.outputs import AssistantOutput
from modules.assistant.ito.audio_transcript import audio_transcript_inputs
from modules.assistant.ito.crawler import crawler_inputs
from modules.assistant.ito.summary import summary_inputs
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
    crawler = crawler_inputs()
    audio_transcript = audio_transcript_inputs()
    return [summary, crawler, audio_transcript]


@assistant_router.post(
    "/assistant/process",
    dependencies=[Depends(AuthBearer())],
    tags=["Assistant"],
)
async def process_assistant(
    values: InputAssistant,
    files: List[UploadFile] = File(None),
    current_user: UserIdentity = Depends(get_current_user),
):
    logger.info(f"Processing assistant with inputs: {values}")
    # if ingestion_id is None:
    #     raise ValueError("Ingestion ID is required")

    # assistant = assistant_service.get_assistant_by_id(ingestion_id)

    # if assistant.name == "summary":
    #     summary = SummaryAssistant(
    #         uploadFile=file_1,
    #         current_user=current_user,
    #         brain_id=brain_id,
    #         send_file_email=send_file_email,
    #         url=url,
    #     )
    #     return await summary.process_assistant()

    # if assistant.name == "audio_transcript":
    #     audio_summary = AudioTranscriptAssistant(
    #         uploadFile=file_1,
    #         current_user=current_user,
    #         brain_id=brain_id,
    #         send_file_email=send_file_email,
    #         url=url,
    #     )
    #     return await audio_summary.process_assistant()

    # if assistant.name == "crawler":
    #     crawler = CrawlerAssistant(
    #         uploadFile=file_1,
    #         current_user=current_user,
    #         brain_id=brain_id,
    #         send_file_email=send_file_email,
    #         url=url,
    #     )
    #     return await crawler.process_assistant()

    return {"message": "Not found"}
