import os

from auth.auth_bearer import AuthBearer, get_current_user
from fastapi import APIRouter, Depends, Request, UploadFile
from models.users import User
from utils.file import convert_bytes, get_file_size
from utils.processors import filter_file
from utils.vectors import CommonsDep

upload_router = APIRouter()

def get_user_vectors(commons, user):
    user_vectors_response = commons['supabase'].table("vectors").select(
        "name:metadata->>file_name, size:metadata->>file_size", count="exact") \
            .filter("user_id", "eq", user.email)\
            .execute()
    documents = user_vectors_response.data  # Access the data from the response
    # Convert each dictionary to a tuple of items, then to a set to remove duplicates, and then back to a dictionary
    user_unique_vectors = [dict(t) for t in set(tuple(d.items()) for d in documents)]
    return user_unique_vectors

def calculate_remaining_space(request, max_brain_size, max_brain_size_with_own_key, current_brain_size):
    remaining_free_space = float(max_brain_size_with_own_key) - current_brain_size if request.headers.get('Openai-Api-Key') else float(max_brain_size) - current_brain_size
    return remaining_free_space

@upload_router.post("/upload", dependencies=[Depends(AuthBearer())], tags=["Upload"])
async def upload_file(request: Request, commons: CommonsDep,  file: UploadFile, enable_summarization: bool = False, current_user: User = Depends(get_current_user)):
    """
    Upload a file to the user's storage.

    - `file`: The file to be uploaded.
    - `enable_summarization`: Flag to enable summarization of the file's content.
    - `current_user`: The current authenticated user.
    - Returns the response message indicating the success or failure of the upload.

    This endpoint allows users to upload files to their storage (brain). It checks the remaining free space in the user's storage (brain)
    and ensures that the file size does not exceed the maximum capacity. If the file is within the allowed size limit,
    it can optionally apply summarization to the file's content. The response message will indicate the status of the upload.
    """
    max_brain_size = os.getenv("MAX_BRAIN_SIZE")
    max_brain_size_with_own_key = os.getenv("MAX_BRAIN_SIZE_WITH_KEY", 209715200)
    
    user_unique_vectors = get_user_vectors(commons, current_user)
    current_brain_size = sum(float(doc['size']) for doc in user_unique_vectors)

    remaining_free_space = calculate_remaining_space(request, max_brain_size, max_brain_size_with_own_key, current_brain_size)

    file_size = get_file_size(file)

    if remaining_free_space - file_size < 0:
        message = {"message": f"❌ User's brain will exceed maximum capacity with this upload. Maximum file allowed is : {convert_bytes(remaining_free_space)}", "type": "error"}
    else: 
        message = await filter_file(file, enable_summarization, commons['supabase'], current_user, openai_api_key=request.headers.get('Openai-Api-Key', None))
 
    return message
