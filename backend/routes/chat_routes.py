import os
import time
from http.client import HTTPException
from typing import List
from uuid import UUID

from auth.auth_bearer import AuthBearer, get_current_user
from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import StreamingResponse
from llm.brainpicking import BrainPicking
from llm.BrainPickingOpenAIFunctions.BrainPickingOpenAIFunctions import (
    BrainPickingOpenAIFunctions,
)
from llm.PrivateBrainPicking import PrivateBrainPicking
from models.chat import Chat, ChatHistory
from models.chats import ChatQuestion
from models.settings import LLMSettings, common_dependencies
from models.users import User
from repository.chat.create_chat import CreateChatProperties, create_chat
from repository.chat.get_chat_by_id import get_chat_by_id
from repository.chat.get_chat_history import get_chat_history
from repository.chat.get_user_chats import get_user_chats
from repository.chat.update_chat import ChatUpdatableProperties, update_chat
from repository.chat.update_chat_history import update_chat_history
from utils.constants import (
    openai_function_compatible_models,
    streaming_compatible_models,
)

chat_router = APIRouter()


def get_chat_details(commons, chat_id):
    response = (
        commons["supabase"]
        .from_("chats")
        .select("*")
        .filter("chat_id", "eq", chat_id)
        .execute()
    )
    return response.data


def delete_chat_from_db(commons, chat_id):
    try:
        commons["supabase"].table("chat_history").delete().match(
            {"chat_id": chat_id}
        ).execute()
    except Exception as e:
        print(e)
        pass
    try:
        commons["supabase"].table("chats").delete().match(
            {"chat_id": chat_id}
        ).execute()
    except Exception as e:
        print(e)
        pass


def fetch_user_stats(commons, user, date):
    response = (
        commons["supabase"]
        .from_("users")
        .select("*")
        .filter("email", "eq", user.email)
        .filter("date", "eq", date)
        .execute()
    )
    userItem = next(iter(response.data or []), {"requests_count": 0})
    return userItem


def check_user_limit(
    user: User,
):
    if user.user_openai_api_key is None:
        date = time.strftime("%Y%m%d")
        max_requests_number = os.getenv("MAX_REQUESTS_NUMBER", 1000)

        user.increment_user_request_count(date)
        if user.requests_count >= max_requests_number:
            raise HTTPException(
                status_code=429,
                detail="You have reached the maximum number of requests for today.",
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
    chats = get_user_chats(current_user.id)
    return {"chats": chats}


# delete one chat
@chat_router.delete(
    "/chat/{chat_id}", dependencies=[Depends(AuthBearer())], tags=["Chat"]
)
async def delete_chat(chat_id: UUID):
    """
    Delete a specific chat by chat ID.
    """
    commons = common_dependencies()
    delete_chat_from_db(commons, chat_id)
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

    chat = get_chat_by_id(chat_id)
    if current_user.id != chat.user_id:
        raise HTTPException(
            status_code=403, detail="You should be the owner of the chat to update it."
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
    "/chat/{chat_id}/question", dependencies=[Depends(AuthBearer())], tags=["Chat"]
)
async def create_question_handler(
    request: Request,
    chat_question: ChatQuestion,
    chat_id: UUID,
    brain_id: UUID = Query(..., description="The ID of the brain"),
    current_user: User = Depends(get_current_user),
) -> ChatHistory:
    current_user.user_openai_api_key = request.headers.get("Openai-Api-Key")
    print("current_user", current_user)
    try:
        check_user_limit(current_user)
        llm_settings = LLMSettings()

        if llm_settings.private:
            gpt_answer_generator = PrivateBrainPicking(
                model=chat_question.model,
                chat_id=str(chat_id),
                temperature=chat_question.temperature,
                max_tokens=chat_question.max_tokens,
                brain_id=brain_id,
                user_openai_api_key=current_user.user_openai_api_key,
            )
            answer = gpt_answer_generator.generate_answer(chat_question.question)

        elif chat_question.model in openai_function_compatible_models:
            # TODO: RBAC with current_user
            gpt_answer_generator = BrainPickingOpenAIFunctions(
                model=chat_question.model,
                chat_id=str(chat_id),
                temperature=chat_question.temperature,
                max_tokens=chat_question.max_tokens,
                # TODO: use user_id in vectors table instead of email
                brain_id=brain_id,
                user_openai_api_key=current_user.user_openai_api_key,
            )
            answer = gpt_answer_generator.generate_answer(chat_question.question)

        else:
            brainPicking = BrainPicking(
                chat_id=str(chat_id),
                model=chat_question.model,
                max_tokens=chat_question.max_tokens,
                temperature=chat_question.temperature,
                brain_id=brain_id,
                user_openai_api_key=current_user.user_openai_api_key,
            )

            answer = brainPicking.generate_answer(chat_question.question)

        chat_answer = update_chat_history(
            chat_id=chat_id,
            user_message=chat_question.question,
            assistant=answer,
        )
        return chat_answer
    except HTTPException as e:
        raise e


# stream new question response from chat
@chat_router.post(
    "/chat/{chat_id}/question/stream",
    dependencies=[Depends(AuthBearer())],
    tags=["Chat"],
)
async def create_stream_question_handler(
    request: Request,
    chat_question: ChatQuestion,
    chat_id: UUID,
    brain_id: UUID = Query(..., description="The ID of the brain"),
    current_user: User = Depends(get_current_user),
) -> StreamingResponse:
    if (
        os.getenv("PRIVATE") == "True"
        or chat_question.model not in streaming_compatible_models
    ):
        # forward the request to the none streaming endpoint create_question_handler function
        return await create_question_handler(
            request, chat_question, chat_id, current_user
        )

    try:
        user_openai_api_key = request.headers.get("Openai-Api-Key")
        check_user_limit(current_user)

        brain = BrainPicking(
            chat_id=str(chat_id),
            model=chat_question.model,
            max_tokens=chat_question.max_tokens,
            temperature=chat_question.temperature,
            brain_id=brain_id,
            user_openai_api_key=user_openai_api_key,
            streaming=True,
        )

        return StreamingResponse(
            brain.generate_stream(chat_question.question),
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
    return get_chat_history(chat_id)
