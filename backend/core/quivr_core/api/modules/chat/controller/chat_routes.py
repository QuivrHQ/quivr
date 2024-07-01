from typing import Annotated, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import StreamingResponse

from quivr_core.api.logger import get_logger
from quivr_core.api.modules.brain.service.brain_service import BrainService
from quivr_core.api.modules.chat.dto.chats import ChatItem, ChatQuestion
from quivr_core.api.modules.chat.dto.inputs import (
    ChatMessageProperties,
    ChatUpdatableProperties,
    CreateChatProperties,
    QuestionAndAnswer,
)
from quivr_core.api.modules.chat.entity.chat import Chat
from quivr_core.api.modules.chat.service.chat_service import ChatService
from quivr_core.api.modules.dependencies import get_current_user, get_service
from quivr_core.api.modules.knowledge.repository.knowledges import KnowledgeRepository
from quivr_core.api.modules.prompt.service.prompt_service import PromptService
from quivr_core.api.modules.rag.rag_service import RAGService
from quivr_core.api.modules.user.entity.user_identity import UserIdentity
from quivr_core.api.packages.utils.telemetry import maybe_send_telemetry

logger = get_logger(__name__)

brain_service = BrainService()
knowledge_service = KnowledgeRepository()


ChatServiceDep = Annotated[ChatService, Depends(get_service(ChatService))]
UserIdentityDep = Annotated[UserIdentity, Depends(get_current_user)]
PromptServiceDep = Annotated[PromptService, Depends(get_service(PromptService))]


chat_router = APIRouter()


@chat_router.get("/chat/healthz", tags=["Health"])
async def healthz():
    return {"status": "ok"}


# get all chats
@chat_router.get("/chat", tags=["Chat"])
async def get_chats(current_user: UserIdentityDep, chat_service: ChatServiceDep):
    """
    Retrieve all chats for the current user.

    - `current_user`: The current authenticated user.
    - Returns a list of all chats for the user.

    This endpoint retrieves all the chats associated with the current authenticated user. It returns a list of chat objects
    containing the chat ID and chat name for each chat.
    """
    chats = await chat_service.get_user_chats(current_user.id)
    return {"chats": chats}


# delete one chat
@chat_router.delete("/chat/{chat_id}", tags=["Chat"])
async def delete_chat(chat_id: UUID, chat_service: ChatServiceDep):
    """
    Delete a specific chat by chat ID.
    """

    chat_service.delete_chat_from_db(chat_id)
    return {"message": f"{chat_id}  has been deleted."}


# update existing chat metadata
@chat_router.put("/chat/{chat_id}/metadata", tags=["Chat"])
async def update_chat_metadata_handler(
    chat_data: ChatUpdatableProperties,
    chat_id: UUID,
    current_user: UserIdentityDep,
    chat_service: ChatServiceDep,
):
    """
    Update chat attributes
    """

    chat = await chat_service.get_chat_by_id(chat_id)
    if str(current_user.id) != chat.user_id:
        raise HTTPException(
            status_code=403,  # pyright: ignore reportPrivateUsage=none
            detail="You should be the owner of the chat to update it.",  # pyright: ignore reportPrivateUsage=none
        )
    return chat_service.update_chat(chat_id=chat_id, chat_data=chat_data)


# update existing message
@chat_router.put("/chat/{chat_id}/{message_id}", tags=["Chat"])
async def update_chat_message(
    chat_message_properties: ChatMessageProperties,
    chat_id: UUID,
    message_id: UUID,
    current_user: UserIdentityDep,
    chat_service: ChatServiceDep,
):
    chat = await chat_service.get_chat_by_id(chat_id)
    if str(current_user.id) != chat.user_id:
        raise HTTPException(
            status_code=403, detail="You should be the owner of the chat to update it."
        )
    return chat_service.update_chat_message(
        chat_id=chat_id,
        message_id=message_id,
        chat_message_properties=chat_message_properties,
    )


# create new chat
@chat_router.post("/chat", tags=["Chat"])
async def create_chat_handler(
    chat_data: CreateChatProperties,
    current_user: UserIdentityDep,
    chat_service: ChatServiceDep,
):
    """
    Create a new chat with initial chat messages.
    """

    return await chat_service.create_chat(
        user_id=current_user.id, new_chat_data=chat_data
    )


# add new question to chat
@chat_router.post(
    "/chat/{chat_id}/question",
    tags=["Chat"],
)
async def create_question_handler(
    request: Request,
    chat_question: ChatQuestion,
    chat_id: UUID,
    current_user: UserIdentityDep,
    chat_service: ChatServiceDep,
    prompt_service: PromptServiceDep,
    brain_id: Annotated[UUID | None, Query()] = None,
):
    try:
        rag_service = RAGService(
            current_user,
            brain_id,
            chat_id,
            brain_service,
            prompt_service,
            chat_service,
            knowledge_service,
        )
        chat_answer = await rag_service.generate_answer(chat_question.question)

        maybe_send_telemetry("question_asked", {"streaming": False}, request)
        return chat_answer

    except AssertionError:
        raise HTTPException(
            status_code=422,
            detail="inprocessable entity",
        )
    except HTTPException as e:
        raise e


# stream new question response from chat
@chat_router.post(
    "/chat/{chat_id}/question/stream",
    tags=["Chat"],
)
async def create_stream_question_handler(
    request: Request,
    chat_question: ChatQuestion,
    chat_id: UUID,
    chat_service: ChatServiceDep,
    current_user: UserIdentityDep,
    prompt_service: PromptServiceDep,
    brain_id: Annotated[UUID | None, Query()] = None,
) -> StreamingResponse:
    logger.info(
        f"Creating question for chat {chat_id} with brain {brain_id} of type {type(brain_id)}"
    )

    rag_service = RAGService(
        current_user,
        brain_id,
        chat_id,
        brain_service,
        prompt_service,
        chat_service,
        knowledge_service,
    )
    maybe_send_telemetry("question_asked", {"streaming": True}, request)

    return StreamingResponse(
        rag_service.generate_answer_stream(chat_question.question),
        media_type="text/event-stream",
    )


# get chat history
@chat_router.get("/chat/{chat_id}/history", tags=["Chat"])
async def get_chat_history_handler(
    chat_id: UUID,
    chat_service: ChatServiceDep,
) -> List[ChatItem]:
    return await chat_service.get_chat_history_with_notifications(chat_id)


@chat_router.post(
    "/chat/{chat_id}/question/answer",
    tags=["Chat"],
)
async def add_question_and_answer_handler(
    chat_id: UUID,
    question_and_answer: QuestionAndAnswer,
    chat_service: ChatServiceDep,
) -> Optional[Chat]:
    """
    Add a new question and anwser to the chat.
    """
    history = await chat_service.add_question_and_answer(chat_id, question_and_answer)
    # TODO(@aminediro) : Do we need to return the chat ??
    return history.chat
