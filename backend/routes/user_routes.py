
import os
import time

from auth.auth_bearer import JWTBearer
from fastapi import APIRouter, Depends, Request
from models.users import User
from utils.vectors import CommonsDep

user_router = APIRouter()
max_brain_size_with_own_key = os.getenv("MAX_BRAIN_SIZE_WITH_KEY",209715200)
@user_router.get("/user", dependencies=[Depends(JWTBearer())])
async def get_user_endpoint(request: Request,commons: CommonsDep, credentials: dict = Depends(JWTBearer())):
    
    # Create a function that returns the unique documents out of the vectors 
    # Create a function that returns the list of documents that can take in what to put in the select + the filter 
    user = User(email=credentials.get('email', 'none'))
    # Cascade delete the summary from the database first, because it has a foreign key constraint
    user_vectors_response = commons['supabase'].table("vectors").select(
        "name:metadata->>file_name, size:metadata->>file_size", count="exact") \
            .filter("user_id", "eq", user.email)\
            .execute()
    documents = user_vectors_response.data  # Access the data from the response
    # Convert each dictionary to a tuple of items, then to a set to remove duplicates, and then back to a dictionary
    user_unique_vectors = [dict(t) for t in set(tuple(d.items()) for d in documents)]

    current_brain_size = sum(float(doc['size']) for doc in user_unique_vectors)

    max_brain_size = os.getenv("MAX_BRAIN_SIZE")
    if request.headers.get('Openai-Api-Key'):
        max_brain_size = max_brain_size_with_own_key

    # Create function get user request stats -> nombre de requetes par jour + max number of requests -> svg to display the number of requests ? une fusee ?
    user = User(email=credentials.get('email', 'none'))
    date = time.strftime("%Y%m%d")
    max_requests_number = os.getenv("MAX_REQUESTS_NUMBER")

    if request.headers.get('Openai-Api-Key'):
        max_brain_size = max_brain_size_with_own_key

    requests_stats = commons['supabase'].from_('users').select(
    '*').filter("email", "eq", user.email).execute()

    return {"email":user.email, 
            "max_brain_size": max_brain_size, 
            "current_brain_size": current_brain_size, 
            "max_requests_number": max_requests_number,
            "requests_stats" : requests_stats.data,
            "date": date,
            }

