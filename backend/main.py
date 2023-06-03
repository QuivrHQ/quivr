import os
import shutil
import time
from tempfile import SpooledTemporaryFile

import pypandoc
from auth.auth_bearer import JWTBearer
from crawl.crawler import CrawlWebsite
from fastapi import Depends, FastAPI, UploadFile
from llm.qa import get_qa_llm
from llm.summarization import llm_evaluate_summaries
from logger import get_logger
from middlewares.cors import add_cors_middleware
from models.chats import ChatMessage
from models.users import User
from pydantic import BaseModel
from supabase import Client
from utils.file import convert_bytes, get_file_size
from utils.processors import filter_file
from utils.vectors import (CommonsDep, create_user, similarity_search,
                           update_user_request_count)

logger = get_logger(__name__)

app = FastAPI()


add_cors_middleware(app)



@app.on_event("startup")
async def startup_event():
    pypandoc.download_pandoc()




@app.post("/upload", dependencies=[Depends(JWTBearer())])
async def upload_file(commons: CommonsDep,  file: UploadFile, enable_summarization: bool = False, credentials: dict = Depends(JWTBearer())):
    max_brain_size = os.getenv("MAX_BRAIN_SIZE")
   
    user = User(email=credentials.get('email', 'none'))
    user_vectors_response = commons['supabase'].table("vectors").select(
        "name:metadata->>file_name, size:metadata->>file_size", count="exact") \
            .filter("user_id", "eq", user.email)\
            .execute()
    documents = user_vectors_response.data  # Access the data from the response
    # Convert each dictionary to a tuple of items, then to a set to remove duplicates, and then back to a dictionary
    user_unique_vectors = [dict(t) for t in set(tuple(d.items()) for d in documents)]

    current_brain_size = sum(float(doc['size']) for doc in user_unique_vectors)

    file_size = get_file_size(file)

    remaining_free_space =  float(max_brain_size) - (current_brain_size)

    if remaining_free_space - file_size < 0:
        message = {"message": f"❌ User's brain will exceed maximum capacity with this upload. Maximum file allowed is : {convert_bytes(remaining_free_space)}", "type": "error"}
    else: 
        message = await filter_file(file, enable_summarization, commons['supabase'], user)
 
    return message


@app.post("/chat/", dependencies=[Depends(JWTBearer())])
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


@app.post("/crawl/", dependencies=[Depends(JWTBearer())])
async def crawl_endpoint(commons: CommonsDep, crawl_website: CrawlWebsite, enable_summarization: bool = False, credentials: dict = Depends(JWTBearer())):
    user = User(email=credentials.get('email', 'none'))
    file_path, file_name = crawl_website.process()

    # Create a SpooledTemporaryFile from the file_path
    spooled_file = SpooledTemporaryFile()
    with open(file_path, 'rb') as f:
        shutil.copyfileobj(f, spooled_file)

    # Pass the SpooledTemporaryFile to UploadFile
    file = UploadFile(file=spooled_file, filename=file_name)
    message = await filter_file(file, enable_summarization, commons['supabase'], user=user)
    return message


@app.get("/explore", dependencies=[Depends(JWTBearer())])
async def explore_endpoint(commons: CommonsDep,credentials: dict = Depends(JWTBearer()) ):
    user = User(email=credentials.get('email', 'none'))
    response = commons['supabase'].table("vectors").select(
        "name:metadata->>file_name, size:metadata->>file_size", count="exact").filter("user_id", "eq", user.email).execute()
    documents = response.data  # Access the data from the response
    # Convert each dictionary to a tuple of items, then to a set to remove duplicates, and then back to a dictionary
    unique_data = [dict(t) for t in set(tuple(d.items()) for d in documents)]
    # Sort the list of documents by size in decreasing order
    unique_data.sort(key=lambda x: int(x['size']), reverse=True)

    return {"documents": unique_data}


@app.delete("/explore/{file_name}", dependencies=[Depends(JWTBearer())])
async def delete_endpoint(commons: CommonsDep, file_name: str, credentials: dict = Depends(JWTBearer())):
    user = User(email=credentials.get('email', 'none'))
    # Cascade delete the summary from the database first, because it has a foreign key constraint
    commons['supabase'].table("summaries").delete().match(
        {"metadata->>file_name": file_name}).execute()
    commons['supabase'].table("vectors").delete().match(
        {"metadata->>file_name": file_name, "user_id": user.email}).execute()
    return {"message": f"{file_name} of user {user.email} has been deleted."}


@app.get("/explore/{file_name}", dependencies=[Depends(JWTBearer())])
async def download_endpoint(commons: CommonsDep, file_name: str,credentials: dict = Depends(JWTBearer()) ):
    user = User(email=credentials.get('email', 'none'))
    response = commons['supabase'].table("vectors").select(
        "metadata->>file_name, metadata->>file_size, metadata->>file_extension, metadata->>file_url", "content").match({"metadata->>file_name": file_name, "user_id": user.email}).execute()
    documents = response.data
    # Returns all documents with the same file name
    return {"documents": documents}


@app.get("/")
async def root():
    return {"status": "OK"}
