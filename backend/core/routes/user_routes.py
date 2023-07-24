import os
import time

from auth import AuthBearer, get_current_user
from fastapi import APIRouter, Depends, Request
from models.brains import Brain, get_default_user_brain
from models.settings import BrainRateLimiting
from models.users import User

user_router = APIRouter()

MAX_BRAIN_SIZE_WITH_OWN_KEY = int(os.getenv("MAX_BRAIN_SIZE_WITH_KEY", 209715200))


def get_unique_documents(vectors):
    # Convert each dictionary to a tuple of items, then to a set to remove duplicates, and then back to a dictionary
    return [dict(t) for t in set(tuple(d.items()) for d in vectors)]


@user_router.get("/user", dependencies=[Depends(AuthBearer())], tags=["User"])
async def get_user_endpoint(
    request: Request, current_user: User = Depends(get_current_user)
):
    """
    Get user information and statistics.

    - `current_user`: The current authenticated user.
    - Returns the user's email, maximum brain size, current brain size, maximum requests number, requests statistics, and the current date.

    This endpoint retrieves information and statistics about the authenticated user. It includes the user's email, maximum brain size,
    current brain size, maximum requests number, requests statistics, and the current date. The brain size is calculated based on the
    user's uploaded vectors, and the maximum brain size is obtained from the environment variables. The requests statistics provide
    information about the user's API usage.
    """

    max_brain_size = BrainRateLimiting().max_brain_size

    if request.headers.get("Openai-Api-Key"):
        max_brain_size = MAX_BRAIN_SIZE_WITH_OWN_KEY

    date = time.strftime("%Y%m%d")
    max_requests_number = os.getenv("MAX_REQUESTS_NUMBER")
    requests_stats = current_user.get_user_request_stats()
    default_brain = get_default_user_brain(current_user)

    if default_brain:
        defaul_brain_size = Brain(id=default_brain["id"]).brain_size
    else:
        defaul_brain_size = 0

    return {
        "email": current_user.email,
        "max_brain_size": max_brain_size,
        "current_brain_size": defaul_brain_size,
        "max_requests_number": max_requests_number,
        "requests_stats": requests_stats,
        "date": date,
    }
