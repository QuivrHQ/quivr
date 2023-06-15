import os
import time

from auth.auth_bearer import AuthBearer, get_current_user
from fastapi import APIRouter, Depends, Request
from models.users import User
from utils.vectors import CommonsDep

user_router = APIRouter()

MAX_BRAIN_SIZE_WITH_OWN_KEY = int(os.getenv("MAX_BRAIN_SIZE_WITH_KEY", 209715200))

def get_unique_documents(vectors):
    # Convert each dictionary to a tuple of items, then to a set to remove duplicates, and then back to a dictionary
    return [dict(t) for t in set(tuple(d.items()) for d in vectors)]

def get_user_vectors(commons, email):
    # Access the supabase table and get the vectors
    user_vectors_response = commons['supabase'].table("vectors").select(
        "name:metadata->>file_name, size:metadata->>file_size", count="exact") \
            .filter("user_id", "eq", email)\
            .execute()
    return user_vectors_response.data

def get_user_request_stats(commons, email):
    requests_stats = commons['supabase'].from_('users').select(
        '*').filter("email", "eq", email).execute()
    return requests_stats.data

@user_router.get("/user", dependencies=[Depends(AuthBearer())], tags=["User"])
async def get_user_endpoint(request: Request, commons: CommonsDep, current_user: User = Depends(get_current_user)):
    """
    Get user information and statistics.

    - `current_user`: The current authenticated user.
    - Returns the user's email, maximum brain size, current brain size, maximum requests number, requests statistics, and the current date.

    This endpoint retrieves information and statistics about the authenticated user. It includes the user's email, maximum brain size,
    current brain size, maximum requests number, requests statistics, and the current date. The brain size is calculated based on the
    user's uploaded vectors, and the maximum brain size is obtained from the environment variables. The requests statistics provide
    information about the user's API usage.
    """
    user_vectors = get_user_vectors(commons, current_user.email)
    user_unique_vectors = get_unique_documents(user_vectors)

    current_brain_size = sum(float(doc.get('size', 0)) for doc in user_unique_vectors)

    max_brain_size = int(os.getenv("MAX_BRAIN_SIZE", 0))
    if request.headers.get('Openai-Api-Key'):
        max_brain_size = MAX_BRAIN_SIZE_WITH_OWN_KEY

    date = time.strftime("%Y%m%d")
    max_requests_number = os.getenv("MAX_REQUESTS_NUMBER")
    
    requests_stats = get_user_request_stats(commons, current_user.email)

    return {"email": current_user.email, 
            "max_brain_size": max_brain_size, 
            "current_brain_size": current_brain_size, 
            "max_requests_number": max_requests_number,
            "requests_stats" : requests_stats,
            "date": date,
            }
