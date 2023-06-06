import os
import time

from auth.auth_bearer import JWTBearer
from fastapi import APIRouter, Depends
from llm.qa import get_qa_llm
from llm.summarization import llm_evaluate_summaries
from models.chats import ChatMessage
from models.users import User
from utils.vectors import (CommonsDep, create_user, similarity_search,
                           update_user_request_count)

chat_router = APIRouter()

@chat_router.post("/chat/", dependencies=[Depends(JWTBearer())])
async def chat_endpoint(commons: CommonsDep, chat_message: ChatMessage, credentials: dict = Depends(JWTBearer())):
    user = User(email=credentials.get('email', 'none'))
    date = time.strftime("%Y%m%d")
    max_requests_number = os.getenv("MAX_REQUESTS_NUMBER")
    response = commons['supabase'].from_('users').select(
    '*').filter("user_id", "eq", user.email).filter("date", "eq", date).execute()


    userItem = next(iter(response.data or []), {"requests_count": 0})
    old_request_count = userItem['requests_count']

    history = chat_message.history
    history.append(("user", chat_message.question))

    qa = get_qa_llm(chat_message, user.email)

    if old_request_count == 0: 
        create_user(user_id= user.email, date=date)
    elif  old_request_count <  float(max_requests_number) : 
        update_user_request_count(user_id=user.email,  date=date, requests_count= old_request_count+1)
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

    return {"history": history}
