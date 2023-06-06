import os
import time
from uuid import UUID

from auth.auth_bearer import JWTBearer
from fastapi import APIRouter, Depends, HTTPException
from llm.qa import get_qa_llm
from llm.summarization import llm_evaluate_summaries
from models.chats import ChatMessage
from models.users import User
from utils.vectors import (CommonsDep, create_chat, create_user,
                           similarity_search, update_chat,
                           update_user_request_count)

chat_router = APIRouter()

# continue chatting
@chat_router.post("/chat/{chat_id}", dependencies=[Depends(JWTBearer())])
async def chat_endpoint(commons: CommonsDep, chat_id: UUID, chat_message: ChatMessage, credentials: dict = Depends(JWTBearer())):
    user = User(email=credentials.get('email', 'none'))
    date = time.strftime("%Y%m%d")
    max_requests_number = os.getenv("MAX_REQUESTS_NUMBER")
    response = commons['supabase'].from_('users').select(
    '*').filter("email", "eq", user.email).filter("date", "eq", date).execute()


    userItem = next(iter(response.data or []), {"requests_count": 0})
    old_request_count = userItem['requests_count']

    history = chat_message.history
    history.append(("user", chat_message.question))

    qa = get_qa_llm(chat_message, user.email)

    if old_request_count == 0: 
        create_user(email= user.email, date=date)
    elif  old_request_count <  float(max_requests_number) : 
        update_user_request_count(email=user.email,  date=date, requests_count= old_request_count+1)
    else: 
        history.append(('assistant', "You have reached your requests limit"))
        return {"history": history }


    if chat_message.use_summarization:
        # 1. get summaries from the vector store based on question
        summaries = similarity_search(
            chat_message.question, table='match_summaries')
        # 2. evaluate summaries against the question
        evaluations = llm_evaluate_summaries(
            chat_message.question, summaries, chat_message.model)
        # 3. pull in the top documents from summaries
        logger.info('Evaluations: %s', evaluations)
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
    history.append(("assistant", model_response["answer"]))

    print('CHAT_ID:', chat_id)
    # Use the chat_id to update the chats table with this history
    update_chat(chat_id=chat_id, history=history)
    print('HISTORY', history)
    return {"history": history}

# new chat 
@chat_router.post("/chat/", dependencies=[Depends(JWTBearer())])
async def chat_endpoint(commons: CommonsDep, chat_message: ChatMessage, credentials: dict = Depends(JWTBearer())):
    date = time.strftime("%Y%m%d")
    user = User(email=credentials.get('email', 'none'))

    # Fetch the user's UUID based on their email
    response = commons['supabase'].from_('users').select('user_id').filter("email", "eq", user.email).execute()

    userItem = next(iter(response.data or []), {})

    if userItem == {}: 
        create_user_response = create_user(email= user.email, date=date)
        user_id = create_user_response.data[0]['user_id']

    else: 
        user_id = userItem['user_id']

    create_chat_response = create_chat(user_id)

    return {"chat_id": create_chat_response.data[0]['chat_id']}

@chat_router.get("/chats/", dependencies=[Depends(JWTBearer())])
async def get_chats(commons: CommonsDep, credentials: dict = Depends(JWTBearer())):
    email = User(email=credentials.get('email', 'none'))

    # Fetch the user's UUID based on their email
    response = commons['supabase'].from_('users').select('user_id').filter("email", "eq", email).execute()
    user_id = response.data[0]['user_id']
    
    # Fetch all chats for the user
    response = commons['supabase'].from_('chats').select('*').filter("user_id", "eq", user_id).execute()
    chats = response.data

    return {"chats": chats}

@chat_router.delete("/chats/{chat_id}", dependencies=[Depends(JWTBearer())])
async def delete_chat(commons: CommonsDep,chat_id: UUID):
    commons['supabase'].table("chats").delete().match(
        {"chat_id": chat_id}).execute()

    return {"message": f"{chat_id}  has been deleted."}
