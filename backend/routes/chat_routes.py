import os
import time
from uuid import UUID
from models.chats import ChatHistory
from auth.auth_bearer import AuthBearer, get_current_user
from fastapi import APIRouter, Depends, Request
from llm.brainpicking import BrainPicking
from models.chats import ChatMessage, ChatAttributes, ChatQuestion, CreateChat
from models.settings import CommonsDep, common_dependencies
from models.users import User
from repository.chat.get_chat_history import get_chat_history
from utils.chats import create_chat, get_chat_name_from_first_question, update_chat
from utils.users import (
    create_user,
    fetch_user_id_from_credentials,
    update_user_request_count,
)

from repository.chat.update_chat_history import update_chat_history

from http.client import HTTPException
from llm.GPTAnswerGenerator.GPTAnswerGenerator import GPTAnswerGenerator

chat_router = APIRouter()


def get_user_chats(commons, user_id):
    response = (
        commons["supabase"]
        .from_("chats")
        .select("chatId:chat_id, chatName:chat_name")
        .filter("user_id", "eq", user_id)
        .execute()
    )
    return response.data


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
    chats = get_user_chats(commons, user_id)
    return {"chats": chats}


# get one chat
@chat_router.get("/chat/{chat_id}", dependencies=[Depends(AuthBearer())], tags=["Chat"])
async def get_chat_handler(chat_id: UUID):
    """
    Retrieve details of a specific chat by chat ID.

    - `chat_id`: The ID of the chat to retrieve details for.
    - Returns the chat ID and its history.

    This endpoint retrieves the details of a specific chat identified by the provided chat ID. It returns the chat ID and its
    history, which includes the chat messages exchanged in the chat.
    """
    commons = common_dependencies()
    chats = get_chat_details(commons, chat_id)
    if len(chats) > 0:
        return {"chatId": chat_id, "history": chats[0]["history"]}
    else:
        return {"error": "Chat not found"}


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


# helper method for update and create chat
def chat_handler(
    request, commons, chat_id, chat_message: ChatMessage, email, is_new_chat=False
):
    date = time.strftime("%Y%m%d")
    user_id = fetch_user_id_from_credentials(commons, {"email": email})
    max_requests_number = os.getenv("MAX_REQUESTS_NUMBER")
    user_openai_api_key = request.headers.get("Openai-Api-Key")

    userItem = fetch_user_stats(commons, User(email=email), date)
    old_request_count = userItem["requests_count"]

    history = chat_message.history
    history.append(("user", chat_message.question))

    chat_name = chat_message.chat_name

    if old_request_count == 0:
        create_user(commons, email=email, date=date)
    else:
        update_user_request_count(
            commons, email, date, requests_count=old_request_count + 1
        )
    if user_openai_api_key is None and old_request_count >= float(max_requests_number):
        history.append(("assistant", "You have reached your requests limit"))
        update_chat(commons, chat_id=chat_id, history=history, chat_name=chat_name)
        return {"history": history}

    brainPicking = BrainPicking(
        chat_id=str(chat_id),
        model=chat_message.model,
        max_tokens=chat_message.max_tokens,
        user_id=user_id,
    )
    answer = brainPicking.generate_answer(chat_message.question)
    history.append(("assistant", answer))

    if is_new_chat:
        chat_name = get_chat_name_from_first_question(chat_message)
        new_chat = create_chat(user_id, chat_name)
        chat_id = new_chat["chat_id"]
    else:
        update_chat(commons, chat_id=chat_id, history=history, chat_name=chat_name)

    return {"history": history, "chatId": chat_id}


# update existing chat
@chat_router.put("/chat/{chat_id}", dependencies=[Depends(AuthBearer())], tags=["Chat"])
async def chat_endpoint(
    request: Request,
    commons: CommonsDep,
    chat_id: UUID,
    chat_message: ChatMessage,
    current_user: User = Depends(get_current_user),
):
    """
    Update an existing chat with new chat messages.
    """
    return chat_handler(request, commons, chat_id, chat_message, current_user.email)


# update existing chat
@chat_router.put(
    "/chat/{chat_id}/metadata", dependencies=[Depends(AuthBearer())], tags=["Chat"]
)
async def update_chat_attributes_handler(
    commons: CommonsDep,
    chat_message: ChatAttributes,
    chat_id: UUID,
    current_user: User = Depends(get_current_user),
):
    """
    Update chat attributes
    """

    user_id = fetch_user_id_from_credentials(commons, {"email": current_user.email})
    chat = get_chat_details(commons, chat_id)[0]
    if user_id != chat.get("user_id"):
        raise HTTPException(status_code=403, detail="Chat not owned by user")
    return update_chat(
        commons=commons, chat_id=chat_id, chat_name=chat_message.chat_name
    )


# create new chat
@chat_router.post("/chat", dependencies=[Depends(AuthBearer())], tags=["Chat"])
async def create_chat_handler(
    chat: CreateChat,
    current_user: User = Depends(get_current_user),
):
    """
    Create a new chat with initial chat messages.
    """
    commons = common_dependencies()
    user_id = fetch_user_id_from_credentials(commons, {"email": current_user.email})
    return create_chat(
        user_id=user_id,
        chat_name=chat.name,
    )


# create new chat
@chat_router.post(
    "/chat/{chat_id}/question", dependencies=[Depends(AuthBearer())], tags=["Chat"]
)
async def create_question_handler(
    chat_question: ChatQuestion,
    chat_id: UUID,
    current_user: User = Depends(get_current_user),
) -> ChatHistory:
    openai_function_compatible_models = [
        "gpt-3.5-turbo-0613",
        "gpt-4-0613",
    ]
    if chat_question.model in openai_function_compatible_models:
        # TODO: RBAC with current_user
        gpt_answer_generator = GPTAnswerGenerator(
            model=chat_question.model,
            chat_id=chat_id,
            temperature=chat_question.temperature,
            max_tokens=chat_question.max_tokens,
            # TODO: use user_id in vectors table instead of email
            user_email=current_user.email,
        )
        answer = gpt_answer_generator.get_answer(chat_question.question)
    else:
        brainPicking = BrainPicking(
            chat_id=str(chat_id),
            model=chat_question.model,
            max_tokens=chat_question.max_tokens,
            user_id=current_user.email,
        )
        answer = brainPicking.generate_answer(chat_question.question)

    chat_answer = update_chat_history(
        chat_id=chat_id, user_message=chat_question.question, assistant_answer=answer
    )
    return chat_answer


# create new chat
@chat_router.get(
    "/chat/{chat_id}/history", dependencies=[Depends(AuthBearer())], tags=["Chat"]
)
async def get_chat_history_handler(
    chat_id: UUID,
    current_user: User = Depends(get_current_user),
) -> list[ChatHistory]:
    # TODO: RBAC with current_user
    return get_chat_history(chat_id)
