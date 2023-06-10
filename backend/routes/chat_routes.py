import os
import time
from typing import Optional
from uuid import UUID

from auth.auth_bearer import JWTBearer
from fastapi import APIRouter, Depends
from llm.qa import get_qa_llm
from llm.summarization import llm_evaluate_summaries
from models.chats import ChatMessage
from models.users import User
from utils.vectors import (CommonsDep, create_chat, create_user,
                           fetch_user_id_from_credentials, similarity_search,
                           update_chat, update_user_request_count)

chat_router = APIRouter()

# get all chats
@chat_router.get("/chat", dependencies=[Depends(JWTBearer())])
async def get_chats(commons: CommonsDep, credentials: dict = Depends(JWTBearer())):
    user_id = fetch_user_id_from_credentials(commons, credentials)
    
    # Fetch all chats for the user
    response = commons['supabase'].from_('chats').select('chatId:chat_id, history').filter("user_id", "eq", user_id).execute()
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
async def chat_endpoint(commons: CommonsDep,  chat_id: UUID, chat_message: ChatMessage, credentials: dict = Depends(JWTBearer())):
    user = User(email=credentials.get('email', 'none'))
    date = time.strftime("%Y%m%d")
    max_requests_number = os.getenv("MAX_REQUESTS_NUMBER")
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

    model_response = get_model_response(commons, chat_message, user.email)
    history.append(("assistant", model_response["answer"]))
    update_chat(chat_id=chat_id, history=history)
    
    return {"history": history}


# create new chat
@chat_router.post("/chat", dependencies=[Depends(JWTBearer())])
async def chat_endpoint(commons: CommonsDep,  chat_message: ChatMessage, credentials: dict = Depends(JWTBearer())):
    user = User(email=credentials.get('email', 'none'))
    user_id = fetch_user_id_from_credentials(commons, credentials)

    date = time.strftime("%Y%m%d")
    max_requests_number = os.getenv("MAX_REQUESTS_NUMBER")
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
        new_chat = create_chat(user_id, history) 
        return {"history": history,  "chatId": new_chat.data[0]['chat_id'] }

    model_response = get_model_response(commons, chat_message, user.email)
    history.append(("assistant", model_response["answer"]))
    new_chat = create_chat(user_id, history)

    return {"history": history, "chatId": new_chat.data[0]['chat_id']}


def get_model_response(commons: CommonsDep,  chat_message: ChatMessage, email: str):
    qa = get_qa_llm(chat_message, email)


    if chat_message.use_summarization:
        # 1. get summaries from the vector store based on question
        summaries = similarity_search(
            chat_message.question, table='match_summaries')
        # 2. evaluate summaries against the question
        evaluations = llm_evaluate_summaries(
            chat_message.question, summaries, chat_message.model)
        # 3. pull in the top documents from summaries
        # logger.info('Evaluations: %s', evaluations)
        if evaluations:
            reponse = commons['supabase'].from_('vectors').select(
                '*').in_('id', values=[e['document_id'] for e in evaluations]).execute()
        # 4. use top docs as additional context
            additional_context = '---\nAdditional Context={}'.format(
                '---\n'.join(data['content'] for data in reponse.data)
            ) + '\n'
        model_response = qa(
            {"question": additional_context + chat_message.question})
    else:
        model_response = qa({"question": chat_message.question})

    return model_response
   