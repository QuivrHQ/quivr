import os
from tempfile import SpooledTemporaryFile

from auth.auth_bearer import JWTBearer
from crawl.crawler import CrawlWebsite
from fastapi import APIRouter, Depends, Request, UploadFile
from models.chats import ChatMessage
from models.users import User
from utils.file import convert_bytes, get_file_size
from utils.processors import filter_file
from utils.vectors import CommonsDep

upload_router = APIRouter()

@upload_router.post("/upload", dependencies=[Depends(JWTBearer())])
async def upload_file(request: Request,commons: CommonsDep,  file: UploadFile, enable_summarization: bool = False, credentials: dict = Depends(JWTBearer())):
    max_brain_size = os.getenv("MAX_BRAIN_SIZE")
    max_brain_size_with_own_key = os.getenv("MAX_BRAIN_SIZE_WITH_KEY",209715200)
    remaining_free_space = 0
    
    user = User(email=credentials.get('email', 'none'))
    user_vectors_response = commons['supabase'].table("vectors").select(
        "name:metadata->>file_name, size:metadata->>file_size", count="exact") \
            .filter("user_id", "eq", user.email)\
            .execute()
    documents = user_vectors_response.data  # Access the data from the response
    # Convert each dictionary to a tuple of items, then to a set to remove duplicates, and then back to a dictionary
    user_unique_vectors = [dict(t) for t in set(tuple(d.items()) for d in documents)]

    current_brain_size = sum(float(doc['size']) for doc in user_unique_vectors)

    if request.headers.get('Openai-Api-Key'):
        remaining_free_space =  float(max_brain_size_with_own_key) - (current_brain_size)
    else:
        remaining_free_space = float(max_brain_size) - (current_brain_size)
    file_size = get_file_size(file)

    if remaining_free_space - file_size < 0:
        message = {"message": f"❌ User's brain will exceed maximum capacity with this upload. Maximum file allowed is : {convert_bytes(remaining_free_space)}", "type": "error"}
    else: 
        message = await filter_file(file, enable_summarization, commons['supabase'], user, openai_api_key=request.headers.get('Openai-Api-Key', None))
 
    return message

