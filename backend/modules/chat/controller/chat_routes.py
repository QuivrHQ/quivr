from typing import Annotated, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import StreamingResponse
from langchain.embeddings.ollama import OllamaEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from logger import get_logger
from middlewares.auth import AuthBearer, get_current_user
from models.settings import BrainSettings, get_supabase_client
from models.user_usage import UserUsage
from modules.brain.service.brain_service import BrainService
from modules.chat.controller.chat.brainful_chat import BrainfulChat
from modules.chat.dto.chats import ChatItem, ChatQuestion
from modules.chat.dto.inputs import (
    ChatMessageProperties,
    ChatUpdatableProperties,
    CreateChatProperties,
    QuestionAndAnswer,
)
from modules.chat.entity.chat import Chat
from modules.chat.service.chat_service import ChatService
from modules.notification.service.notification_service import NotificationService
from modules.user.entity.user_identity import UserIdentity
from packages.utils.telemetry import send_telemetry
from vectorstore.supabase import CustomSupabaseVectorStore

logger = get_logger(__name__)

chat_router = APIRouter()

notification_service = NotificationService()
brain_service = BrainService()
chat_service = ChatService()


def init_vector_store(user_id: UUID) -> CustomSupabaseVectorStore:
    """
    Initialize the vector store
    """
    brain_settings = BrainSettings()
    supabase_client = get_supabase_client()
    embeddings = None
    if brain_settings.ollama_api_base_url:
        embeddings = OllamaEmbeddings(
            base_url=brain_settings.ollama_api_base_url
        )  # pyright: ignore reportPrivateUsage=none
    else:
        embeddings = OpenAIEmbeddings()
    vector_store = CustomSupabaseVectorStore(
        supabase_client, embeddings, table_name="vectors", user_id=user_id
    )

    return vector_store


def get_answer_generator(
    chat_id: UUID,
    chat_question: ChatQuestion,
    brain_id: UUID,
    current_user: UserIdentity,
):
    chat_instance = BrainfulChat()
    chat_instance.validate_authorization(user_id=current_user.id, brain_id=brain_id)

    user_usage = UserUsage(
        id=current_user.id,
        email=current_user.email,
    )

    vector_store = init_vector_store(user_id=current_user.id)

    # Get History
    history = chat_service.get_chat_history(chat_id)

    # Generic
    brain, metadata_brain = brain_service.find_brain_from_question(
        brain_id, chat_question.question, current_user, chat_id, history, vector_store
    )

    send_telemetry("question_asked", {"model_name": brain.model})

    gpt_answer_generator = chat_instance.get_answer_generator(
        brain=brain,
        chat_id=str(chat_id),
        model=brain.model,
        temperature=0.1,
        streaming=True,
        prompt_id=chat_question.prompt_id,
        user_id=current_user.id,
        user_email=current_user.email,
    )

    return gpt_answer_generator


@chat_router.get("/chat/healthz", tags=["Health"])
async def healthz():
    return {"status": "ok"}


# get all chats
@chat_router.get("/chat", dependencies=[Depends(AuthBearer())], tags=["Chat"])
async def get_chats(current_user: UserIdentity = Depends(get_current_user)):
    """
    Retrieve all chats for the current user.

    - `current_user`: The current authenticated user.
    - Returns a list of all chats for the user.

    This endpoint retrieves all the chats associated with the current authenticated user. It returns a list of chat objects
    containing the chat ID and chat name for each chat.
    """
    chats = chat_service.get_user_chats(str(current_user.id))
    return {"chats": chats}


# delete one chat
@chat_router.delete(
    "/chat/{chat_id}", dependencies=[Depends(AuthBearer())], tags=["Chat"]
)
async def delete_chat(chat_id: UUID):
    """
    Delete a specific chat by chat ID.
    """
    notification_service.remove_chat_notifications(chat_id)

    chat_service.delete_chat_from_db(chat_id)
    return {"message": f"{chat_id}  has been deleted."}


# update existing chat metadata
@chat_router.put(
    "/chat/{chat_id}/metadata", dependencies=[Depends(AuthBearer())], tags=["Chat"]
)
async def update_chat_metadata_handler(
    chat_data: ChatUpdatableProperties,
    chat_id: UUID,
    current_user: UserIdentity = Depends(get_current_user),
):
    """
    Update chat attributes
    """

    chat = chat_service.get_chat_by_id(
        chat_id  # pyright: ignore reportPrivateUsage=none
    )
    if str(current_user.id) != chat.user_id:
        raise HTTPException(
            status_code=403,  # pyright: ignore reportPrivateUsage=none
            detail="You should be the owner of the chat to update it.",  # pyright: ignore reportPrivateUsage=none
        )
    return chat_service.update_chat(chat_id=chat_id, chat_data=chat_data)


# update existing message
@chat_router.put(
    "/chat/{chat_id}/{message_id}", dependencies=[Depends(AuthBearer())], tags=["Chat"]
)
async def update_chat_message(
    chat_message_properties: ChatMessageProperties,
    chat_id: UUID,
    message_id: UUID,
    current_user: UserIdentity = Depends(get_current_user),
)  :

    chat = chat_service.get_chat_by_id(
        chat_id  # pyright: ignore reportPrivateUsage=none
    )
    if str(current_user.id) != chat.user_id:
        raise HTTPException(
            status_code=403,  # pyright: ignore reportPrivateUsage=none
            detail="You should be the owner of the chat to update it.",  # pyright: ignore reportPrivateUsage=none
        )
    return chat_service.update_chat_message(
        chat_id=chat_id,
        message_id=message_id,
        chat_message_properties=chat_message_properties.dict(),
    )


# create new chat
@chat_router.post("/chat", dependencies=[Depends(AuthBearer())], tags=["Chat"])
async def create_chat_handler(
    chat_data: CreateChatProperties,
    current_user: UserIdentity = Depends(get_current_user),
):
    """
    Create a new chat with initial chat messages.
    """

    return chat_service.create_chat(user_id=current_user.id, chat_data=chat_data)


# add new question to chat
@chat_router.post(
    "/chat/{chat_id}/question",
    dependencies=[
        Depends(
            AuthBearer(),
        ),
    ],
    tags=["Chat"],
)
async def create_question_handler(
    request: Request,
    chat_question: ChatQuestion,
    chat_id: UUID,
    brain_id: Annotated[UUID | None, Query()] = None,
    current_user: UserIdentity = Depends(get_current_user),
):
    try:
        logger.info(
            f"Creating question for chat {chat_id} with brain {brain_id} of type {type(brain_id)}"
        )
        gpt_answer_generator = get_answer_generator(
            chat_id, chat_question, brain_id, current_user
        )

        chat_answer = gpt_answer_generator.generate_answer(
            chat_id, chat_question, save_answer=True
        )

        return chat_answer
    except HTTPException as e:
        raise e


# stream new question response from chat
@chat_router.post(
    "/chat/{chat_id}/question/stream",
    dependencies=[
        Depends(
            AuthBearer(),
        ),
    ],
    tags=["Chat"],
)
async def create_stream_question_handler(
    request: Request,
    chat_question: ChatQuestion,
    chat_id: UUID,
    brain_id: Annotated[UUID | None, Query()] = None,
    current_user: UserIdentity = Depends(get_current_user),
) -> StreamingResponse:

    chat_instance = BrainfulChat()
    chat_instance.validate_authorization(user_id=current_user.id, brain_id=brain_id)

    user_usage = UserUsage(
        id=current_user.id,
        email=current_user.email,
    )

    logger.info(
        f"Creating question for chat {chat_id} with brain {brain_id} of type {type(brain_id)}"
    )

    gpt_answer_generator = get_answer_generator(
        chat_id, chat_question, brain_id, current_user
    )

    try:
        return StreamingResponse(
            gpt_answer_generator.generate_stream(
                chat_id, chat_question, save_answer=True
            ),
            media_type="text/event-stream",
        )

    except HTTPException as e:
        raise e


# get chat history
@chat_router.get(
    "/chat/{chat_id}/history", dependencies=[Depends(AuthBearer())], tags=["Chat"]
)
async def get_chat_history_handler(
    chat_id: UUID,
) -> List[ChatItem]:
    # TODO: RBAC with current_user
    return chat_service.get_chat_history_with_notifications(chat_id)


@chat_router.post(
    "/chat/{chat_id}/question/answer",
    dependencies=[Depends(AuthBearer())],
    tags=["Chat"],
)
async def add_question_and_answer_handler(
    chat_id: UUID,
    question_and_answer: QuestionAndAnswer,
) -> Optional[Chat]:
    """
    Add a new question and anwser to the chat.
    """
    return chat_service.add_question_and_answer(chat_id, question_and_answer)
