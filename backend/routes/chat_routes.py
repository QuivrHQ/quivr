import os
import time
from typing import Optional
from uuid import UUID

from auth.auth_bearer import JWTBearer
from fastapi import APIRouter, Depends, Request
from models.chats import ChatMessage
from models.users import User
from utils.vectors import (CommonsDep, create_chat, create_user,
                           fetch_user_id_from_credentials, get_answer,
                           get_chat_name_from_first_question, update_chat,
                           update_user_request_count)

chat_router = APIRouter()

# get all chats
@chat_router.get("/chat", dependencies=[Depends(JWTBearer())])
async def get_chats(commons: CommonsDep, credentials: dict = Depends(JWTBearer())):
    date = time.strftime("%Y%m%d")
    user_id = fetch_user_id_from_credentials(commons,date, credentials)
    
    # Fetch all chats for the user
    response = commons['supabase'].from_('chats').select('chatId:chat_id, chatName:chat_name').filter("user_id", "eq", user_id).execute()
    chats = response.data
    # TODO: Only get the chat name instead of the history
    return {"chats": chats}

# get one chat
@chat_router.get("/chat/{chat_id}", dependencies=[Depends(JWTBearer())])
async def get_chats(commons: CommonsDep, chat_id: UUID):
    
    # Fetch all chats for the user
    response = commons['supabase'].from_('chats').select('*').filter("chat_id", "eq", chat_id).execute()
    chats = response.data

    print("/chat/{chat_id}",chats)
    return {"chatId": chat_id, "history": chats[0]['history']}

# delete one chat
@chat_router.delete("/chat/{chat_id}", dependencies=[Depends(JWTBearer())])
async def delete_chat(commons: CommonsDep,chat_id: UUID):
    commons['supabase'].table("chats").delete().match(
        {"chat_id": chat_id}).execute()

    return {"message": f"{chat_id}  has been deleted."}


# update existing chat
@chat_router.put("/chat/{chat_id}", dependencies=[Depends(JWTBearer())])
async def chat_endpoint(request: Request,commons: CommonsDep,  chat_id: UUID, chat_message: ChatMessage, credentials: dict = Depends(JWTBearer())):
    user = User(email=credentials.get('email', 'none'))
    date = time.strftime("%Y%m%d")
    max_requests_number = os.getenv("MAX_REQUESTS_NUMBER")
    user_openai_api_key = request.headers.get('Openai-Api-Key')

    response = commons['supabase'].from_('users').select(
    '*').filter("email", "eq", user.email).filter("date", "eq", date).execute()


    userItem = next(iter(response.data or []), {"requests_count": 0})
    old_request_count = userItem['requests_count']

    history = chat_message.history
    history.append(("user", chat_message.question))

    if old_request_count == 0: 
        create_user(email= user.email, date=date)
    elif  old_request_count <  float(max_requests_number) : 
        update_user_request_count(email=user.email,  date=date, requests_count= old_request_count+1)
    else: 
        history.append(('assistant', "You have reached your requests limit"))
        update_chat(chat_id=chat_id, history=history)
        return {"history": history }

    answer = get_answer(commons, chat_message, user.email,user_openai_api_key)
    history.append(("assistant", answer))
    update_chat(chat_id=chat_id, history=history)
    
    return {"history": history, "chatId": chat_id}


# create new chat
@chat_router.post("/chat", dependencies=[Depends(JWTBearer())])
async def chat_endpoint(request: Request,commons: CommonsDep,  chat_message: ChatMessage, credentials: dict = Depends(JWTBearer())):
    user = User(email=credentials.get('email', 'none'))
    date = time.strftime("%Y%m%d")

    user_id = fetch_user_id_from_credentials(commons, date,credentials)

    max_requests_number = os.getenv("MAX_REQUESTS_NUMBER")
    user_openai_api_key = request.headers.get('Openai-Api-Key')

    response = commons['supabase'].from_('users').select(
    '*').filter("email", "eq", user.email).filter("date", "eq", date).execute()


    userItem = next(iter(response.data or []), {"requests_count": 0})
    old_request_count = userItem['requests_count']

    history = chat_message.history
    history.append(("user", chat_message.question))

    chat_name = get_chat_name_from_first_question(chat_message)
    print('chat_name',chat_name)  
    if user_openai_api_key is None:
        if old_request_count == 0: 
            create_user(email= user.email, date=date)
        elif  old_request_count <  float(max_requests_number) : 
            update_user_request_count(email=user.email,  date=date, requests_count= old_request_count+1)
        else: 
            history.append(('assistant', "You have reached your requests limit"))
            new_chat = create_chat(user_id, history, chat_name) 
            return {"history": history,  "chatId": new_chat.data[0]['chat_id'] }

    answer = get_answer(commons, chat_message, user.email, user_openai_api_key)
    history.append(("assistant", answer))
    new_chat = create_chat(user_id, history, chat_name)

    return {"history": history, "chatId": new_chat.data[0]['chat_id'], "chatName":new_chat.data[0]['chat_name'] }
