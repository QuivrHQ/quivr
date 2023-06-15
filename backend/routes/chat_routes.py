import os
import time
from uuid import UUID

from auth.auth_bearer import AuthBearer, get_current_user
from fastapi import APIRouter, Depends, Request
from models.chats import ChatMessage
from models.users import User
from utils.vectors import (CommonsDep, create_chat, create_user,
                           fetch_user_id_from_credentials, get_answer,
                           get_chat_name_from_first_question, update_chat,
                           update_user_request_count)

chat_router = APIRouter()

def get_user_chats(commons, user_id):
    response = commons['supabase'].from_('chats').select('chatId:chat_id, chatName:chat_name').filter("user_id", "eq", user_id).execute()
    return response.data

def get_chat_details(commons, chat_id):
    response = commons['supabase'].from_('chats').select('*').filter("chat_id", "eq", chat_id).execute()
    return response.data

def delete_chat_from_db(commons, chat_id):
    commons['supabase'].table("chats").delete().match({"chat_id": chat_id}).execute()

def fetch_user_stats(commons, user, date):
    response = commons['supabase'].from_('users').select('*').filter("email", "eq", user.email).filter("date", "eq", date).execute()
    userItem = next(iter(response.data or []), {"requests_count": 0})
    return userItem

# get all chats
@chat_router.get("/chat", dependencies=[Depends(AuthBearer())], tags=["Chat"])
async def get_chats(commons: CommonsDep, current_user: User = Depends(get_current_user)):
    """
    Retrieve all chats for the current user.

    - `current_user`: The current authenticated user.
    - Returns a list of all chats for the user.

    This endpoint retrieves all the chats associated with the current authenticated user. It returns a list of chat objects
    containing the chat ID and chat name for each chat.
    """
    date = time.strftime("%Y%m%d")
    user_id = fetch_user_id_from_credentials(commons, date, {"email": current_user.email})
    chats = get_user_chats(commons, user_id)
    return {"chats": chats}

# get one chat
@chat_router.get("/chat/{chat_id}", dependencies=[Depends(AuthBearer())], tags=["Chat"])
async def get_chats(commons: CommonsDep, chat_id: UUID):
    """
    Retrieve details of a specific chat by chat ID.

    - `chat_id`: The ID of the chat to retrieve details for.
    - Returns the chat ID and its history.

    This endpoint retrieves the details of a specific chat identified by the provided chat ID. It returns the chat ID and its
    history, which includes the chat messages exchanged in the chat.
    """
    chats = get_chat_details(commons, chat_id)
    if len(chats) > 0:
        return {"chatId": chat_id, "history": chats[0]['history']}
    else:
        return {"error": "Chat not found"}

# delete one chat
@chat_router.delete("/chat/{chat_id}", dependencies=[Depends(AuthBearer())], tags=["Chat"])
async def delete_chat(commons: CommonsDep, chat_id: UUID):
    """
    Delete a specific chat by chat ID.
    """
    delete_chat_from_db(commons, chat_id)
    return {"message": f"{chat_id}  has been deleted."}

# helper method for update and create chat
def chat_handler(request, commons, chat_id, chat_message, email, is_new_chat=False):
    date = time.strftime("%Y%m%d")
    user_id = fetch_user_id_from_credentials(commons, date, {"email": email})
    max_requests_number = os.getenv("MAX_REQUESTS_NUMBER")
    user_openai_api_key = request.headers.get('Openai-Api-Key')

    userItem = fetch_user_stats(commons, User(email=email), date)
    old_request_count = userItem['requests_count']

    history = chat_message.history
    history.append(("user", chat_message.question))

    
    if old_request_count == 0: 
        create_user(email= email, date=date)
    else:
        update_user_request_count(email=email, date=date, requests_count=old_request_count + 1)
    if user_openai_api_key is None and old_request_count >= float(max_requests_number):
        history.append(('assistant', "You have reached your requests limit"))
        update_chat(chat_id=chat_id, history=history)
        return {"history": history}



    answer = get_answer(commons, chat_message, email, user_openai_api_key)
    history.append(("assistant", answer))

    if is_new_chat:
        chat_name = get_chat_name_from_first_question(chat_message)
        new_chat = create_chat(user_id, history, chat_name)
        chat_id = new_chat.data[0]['chat_id']
    else:
        update_chat(chat_id=chat_id, history=history)

    return {"history": history, "chatId": chat_id}

# update existing chat
@chat_router.put("/chat/{chat_id}", dependencies=[Depends(AuthBearer())], tags=["Chat"])
async def chat_endpoint(request: Request, commons: CommonsDep, chat_id: UUID, chat_message: ChatMessage, current_user: User = Depends(get_current_user)):
    """
    Update an existing chat with new chat messages.
    """
    return chat_handler(request, commons, chat_id, chat_message, current_user.email)

# create new chat
@chat_router.post("/chat", dependencies=[Depends(AuthBearer())], tags=["Chat"])
async def chat_endpoint(request: Request, commons: CommonsDep, chat_message: ChatMessage, current_user: User = Depends(get_current_user)):
    """
    Create a new chat with initial chat messages.
    """
    return chat_handler(request, commons, None, chat_message, current_user.email, is_new_chat=True)
