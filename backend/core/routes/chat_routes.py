import os
import time
from typing import List
from uuid import UUID
from venv import logger

from auth import AuthBearer, get_current_user
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import StreamingResponse
from llm.openai import OpenAIBrainPicking
from models.brains import Brain
from models.chat import Chat, ChatHistory
from models.chats import ChatQuestion
from models.databases.supabase.supabase import SupabaseDB
from models.settings import LLMSettings, get_supabase_db
from models.users import User
from repository.brain.get_brain_details import get_brain_details
from repository.brain.get_default_user_brain_or_create_new import (
    get_default_user_brain_or_create_new,
)
from repository.chat.create_chat import CreateChatProperties, create_chat
from repository.chat.get_chat_by_id import get_chat_by_id
from repository.chat.get_chat_history import get_chat_history
from repository.chat.get_user_chats import get_user_chats
from repository.chat.update_chat import ChatUpdatableProperties, update_chat
from repository.user_identity.get_user_identity import get_user_identity

chat_router = APIRouter()


class NullableUUID(UUID):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v) -> UUID | None:
        if v == "":
            return None
        try:
            return UUID(v)
        except ValueError:
            return None


def delete_chat_from_db(supabase_db: SupabaseDB, chat_id):
    try:
        supabase_db.delete_chat_history(chat_id)
    except Exception as e:
        print(e)
        pass
    try:
        supabase_db.delete_chat(chat_id)
    except Exception as e:
        print(e)
        pass


def check_user_limit(
    user: User,
):
    if user.user_openai_api_key is None:
        date = time.strftime("%Y%m%d")
        max_requests_number = int(os.getenv("MAX_REQUESTS_NUMBER", 1000))

        user.increment_user_request_count(date)
        if int(user.requests_count) >= int(max_requests_number):
            raise HTTPException(
                status_code=429,  # pyright: ignore reportPrivateUsage=none
                detail="You have reached the maximum number of requests for today.",  # pyright: ignore reportPrivateUsage=none
            )
    else:
        pass


# get all chats
@chat_router.get("/chat", dependencies=[Depends(AuthBearer())], tags=["Chat"])
async def get_chats(current_user: User = Depends(get_current_user)):
    """
    Retrieve all chats for the current user.

    - `current_user`: The current authenticated user.
    - Returns a list of all chats for the user.

    This endpoint retrieves all the chats associated with the current authenticated user. It returns a list of chat objects
    containing the chat ID and chat name for each chat.
    """
    chats = get_user_chats(current_user.id)  # pyright: ignore reportPrivateUsage=none
    return {"chats": chats}


# delete one chat
@chat_router.delete(
    "/chat/{chat_id}", dependencies=[Depends(AuthBearer())], tags=["Chat"]
)
async def delete_chat(chat_id: UUID):
    """
    Delete a specific chat by chat ID.
    """
    supabase_db = get_supabase_db()
    delete_chat_from_db(supabase_db=supabase_db, chat_id=chat_id)
    return {"message": f"{chat_id}  has been deleted."}


# update existing chat metadata
@chat_router.put(
    "/chat/{chat_id}/metadata", dependencies=[Depends(AuthBearer())], tags=["Chat"]
)
async def update_chat_metadata_handler(
    chat_data: ChatUpdatableProperties,
    chat_id: UUID,
    current_user: User = Depends(get_current_user),
) -> Chat:
    """
    Update chat attributes
    """

    chat = get_chat_by_id(chat_id)  # pyright: ignore reportPrivateUsage=none
    if str(current_user.id) != chat.user_id:
        raise HTTPException(
            status_code=403,  # pyright: ignore reportPrivateUsage=none
            detail="You should be the owner of the chat to update it.",  # pyright: ignore reportPrivateUsage=none
        )
    return update_chat(chat_id=chat_id, chat_data=chat_data)


# create new chat
@chat_router.post("/chat", dependencies=[Depends(AuthBearer())], tags=["Chat"])
async def create_chat_handler(
    chat_data: CreateChatProperties,
    current_user: User = Depends(get_current_user),
):
    """
    Create a new chat with initial chat messages.
    """

    return create_chat(user_id=current_user.id, chat_data=chat_data)


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
    brain_id: NullableUUID
    | UUID
    | None = Query(..., description="The ID of the brain"),
    current_user: User = Depends(get_current_user),
) -> ChatHistory:
    """
    Add a new question to the chat.
    """
    # Retrieve user's OpenAI API key
    current_user.user_openai_api_key = request.headers.get("Openai-Api-Key")
    brain = Brain(id=brain_id)

    if not current_user.user_openai_api_key:
        if brain_id:
            brain_details = get_brain_details(brain_id)
            if brain_details:
                current_user.user_openai_api_key = brain_details.openai_api_key

    if not current_user.user_openai_api_key:
        user_identity = get_user_identity(current_user.id)

        if user_identity is not None:
            current_user.user_openai_api_key = user_identity.openai_api_key

    # Retrieve chat model (temperature, max_tokens, model)
    if (
        not chat_question.model
        or not chat_question.temperature
        or not chat_question.max_tokens
    ):
        # TODO: create ChatConfig class (pick config from brain or user or chat) and use it here
        chat_question.model = chat_question.model or brain.model or "gpt-3.5-turbo-0613"
        chat_question.temperature = chat_question.temperature or brain.temperature or 0
        chat_question.max_tokens = chat_question.max_tokens or brain.max_tokens or 256

    try:
        check_user_limit(current_user)
        LLMSettings()

        if not brain_id:
            brain_id = get_default_user_brain_or_create_new(current_user).brain_id

        gpt_answer_generator = OpenAIBrainPicking(
            chat_id=str(chat_id),
            model=chat_question.model,
            max_tokens=chat_question.max_tokens,
            temperature=chat_question.temperature,
            brain_id=str(brain_id),
            user_openai_api_key=current_user.user_openai_api_key,  # pyright: ignore reportPrivateUsage=none
        )

        chat_answer = gpt_answer_generator.generate_answer(  # pyright: ignore reportPrivateUsage=none
            chat_question.question
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
    brain_id: NullableUUID
    | UUID
    | None = Query(..., description="The ID of the brain"),
    current_user: User = Depends(get_current_user),
) -> StreamingResponse:
    # TODO: check if the user has access to the brain

    # Retrieve user's OpenAI API key
    current_user.user_openai_api_key = request.headers.get("Openai-Api-Key")
    brain = Brain(id=brain_id)

    if not current_user.user_openai_api_key and brain_id:
        brain_details = get_brain_details(brain_id)
        if brain_details:
            current_user.user_openai_api_key = brain_details.openai_api_key

    if not current_user.user_openai_api_key:
        user_identity = get_user_identity(current_user.id)

        if user_identity is not None:
            current_user.user_openai_api_key = user_identity.openai_api_key

    # Retrieve chat model (temperature, max_tokens, model)
    if (
        not chat_question.model
        or not chat_question.temperature
        or not chat_question.max_tokens
    ):
        # TODO: create ChatConfig class (pick config from brain or user or chat) and use it here
        chat_question.model = chat_question.model or brain.model or "gpt-3.5-turbo-0613"
        chat_question.temperature = chat_question.temperature or brain.temperature or 0
        chat_question.max_tokens = chat_question.max_tokens or brain.max_tokens or 256

    try:
        logger.info(f"Streaming request for {chat_question.model}")
        check_user_limit(current_user)
        if not brain_id:
            brain_id = get_default_user_brain_or_create_new(current_user).brain_id

        gpt_answer_generator = OpenAIBrainPicking(
            chat_id=str(chat_id),
            model=chat_question.model,
            max_tokens=chat_question.max_tokens,
            temperature=chat_question.temperature,
            brain_id=str(brain_id),
            user_openai_api_key=current_user.user_openai_api_key,  # pyright: ignore reportPrivateUsage=none
            streaming=True,
        )

        print("streaming")
        return StreamingResponse(
            gpt_answer_generator.generate_stream(  # pyright: ignore reportPrivateUsage=none
                chat_question.question
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
) -> List[ChatHistory]:
    # TODO: RBAC with current_user
    return get_chat_history(chat_id)  # pyright: ignore reportPrivateUsage=none
