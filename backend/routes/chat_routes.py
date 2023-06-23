import os
import time
from uuid import UUID

from auth.auth_bearer import AuthBearer, get_current_user
from fastapi import APIRouter, Depends, HTTPException, Request
from llm.brainpicking import BrainPicking
from llm.OpenAiFunctionBasedAnswerGenerator.OpenAiFunctionBasedAnswerGenerator import (
    OpenAiFunctionBasedAnswerGenerator,
)
from models.chat import Chat, ChatHistory
from models.chats import ChatQuestion
from models.settings import common_dependencies
from models.users import User
from repository.chat.create_chat import CreateChatProperties, create_chat
from repository.chat.get_chat_by_id import get_chat_by_id
from repository.chat.get_chat_history import get_chat_history
from repository.chat.get_user_chats import get_user_chats
from repository.chat.update_chat import ChatUpdatableProperties, update_chat
from repository.chat.update_chat_history import update_chat_history
from utils.users import fetch_user_id_from_credentials, update_user_request_count

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
    commons["supabase"].table("chats").delete().match({"chat_id": chat_id}).execute()


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
    commons = common_dependencies()
    user_id = fetch_user_id_from_credentials(commons, {"email": current_user.email})
    chats = get_user_chats(user_id)
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
    commons = common_dependencies()

    user_id = fetch_user_id_from_credentials(commons, {"email": current_user.email})
    chat = get_chat_by_id(chat_id)
    if user_id != chat.user_id:
        raise HTTPException(
            status_code=403, detail="You should be the owner of the chat to update it."
        )
    return update_chat(chat_id=chat_id, chat_data=chat_data)


# helper method for update and create chat
def check_user_limit(
    email,
    user_openai_api_key: str = None,
):
    if user_openai_api_key is None:
        date = time.strftime("%Y%m%d")
        max_requests_number = os.getenv("MAX_REQUESTS_NUMBER")
        commons = common_dependencies()
        userItem = fetch_user_stats(commons, User(email=email), date)
        old_request_count = userItem["requests_count"]

        update_user_request_count(
            commons, email, date, requests_count=old_request_count + 1
        )
        if old_request_count >= float(max_requests_number):
            raise HTTPException(
                status_code=429,
                detail="You have reached the maximum number of requests for today.",
            )
    else:
        pass


# create new chat
@chat_router.post("/chat", dependencies=[Depends(AuthBearer())], tags=["Chat"])
async def create_chat_handler(
    chat_data: CreateChatProperties,
    current_user: User = Depends(get_current_user),
):
    """
    Create a new chat with initial chat messages.
    """

    commons = common_dependencies()
    user_id = fetch_user_id_from_credentials(commons, {"email": current_user.email})
    return create_chat(user_id=user_id, chat_data=chat_data)


# add new question to chat
@chat_router.post(
    "/chat/{chat_id}/question", dependencies=[Depends(AuthBearer())], tags=["Chat"]
)
async def create_question_handler(
    request: Request,
    chat_question: ChatQuestion,
    chat_id: UUID,
    current_user: User = Depends(get_current_user),
) -> ChatHistory:
    try:
        user_openai_api_key = request.headers.get("Openai-Api-Key")
        check_user_limit(current_user.email, user_openai_api_key)
        openai_function_compatible_models = [
            "gpt-3.5-turbo-0613",
            "gpt-4-0613",
        ]
        if chat_question.model in openai_function_compatible_models:
            # TODO: RBAC with current_user
            gpt_answer_generator = OpenAiFunctionBasedAnswerGenerator(
                model=chat_question.model,
                chat_id=chat_id,
                temperature=chat_question.temperature,
                max_tokens=chat_question.max_tokens,
                # TODO: use user_id in vectors table instead of email
                user_email=current_user.email,
                user_openai_api_key=user_openai_api_key,
            )
            answer = gpt_answer_generator.get_answer(chat_question.question)
        else:
            brainPicking = BrainPicking(
                chat_id=str(chat_id),
                model=chat_question.model,
                max_tokens=chat_question.max_tokens,
                user_id=current_user.email,
                user_openai_api_key=user_openai_api_key,
            )
            answer = brainPicking.generate_answer(chat_question.question)

        chat_answer = update_chat_history(
            chat_id=chat_id,
            user_message=chat_question.question,
            assistant_answer=answer,
        )
        return chat_answer
    except HTTPException as e:
        raise e


# get chat history
@chat_router.get(
    "/chat/{chat_id}/history", dependencies=[Depends(AuthBearer())], tags=["Chat"]
)
async def get_chat_history_handler(
    chat_id: UUID,
    current_user: User = Depends(get_current_user),
) -> list[ChatHistory]:
    # TODO: RBAC with current_user
    return get_chat_history(chat_id)
