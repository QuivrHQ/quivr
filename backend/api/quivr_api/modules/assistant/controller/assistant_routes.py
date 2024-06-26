from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from quivr_api.logger import get_logger
from quivr_api.middlewares.auth import AuthBearer, get_current_user
from quivr_api.modules.assistant.dto.inputs import InputAssistant
from quivr_api.modules.assistant.dto.outputs import AssistantOutput
from quivr_api.modules.assistant.ito.difference import DifferenceAssistant
from quivr_api.modules.assistant.ito.summary import SummaryAssistant, summary_inputs
from quivr_api.modules.assistant.service.assistant import Assistant
from quivr_api.modules.user.entity.user_identity import UserIdentity

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
    # difference = difference_inputs()
    # crawler = crawler_inputs()
    # audio_transcript = audio_transcript_inputs()
    return [summary]


@assistant_router.post(
    "/assistant/process",
    dependencies=[Depends(AuthBearer())],
    tags=["Assistant"],
)
async def process_assistant(
    input: InputAssistant,
    files: List[UploadFile] = None,
    current_user: UserIdentity = Depends(get_current_user),
):
    if input.name.lower() == "summary":
        summary_assistant = SummaryAssistant(
            input=input, files=files, current_user=current_user
        )
        try:
            summary_assistant.check_input()
            return await summary_assistant.process_assistant()
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    elif input.name.lower() == "difference":
        difference_assistant = DifferenceAssistant(
            input=input, files=files, current_user=current_user
        )
        try:
            difference_assistant.check_input()
            return await difference_assistant.process_assistant()
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Assistant not found"}
