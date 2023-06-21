
from logger import get_logger
from models.settings import CommonsDep
from models.users import User

logger = get_logger(__name__)

def create_user(commons: CommonsDep, user:User, date):
    logger.info(f"New user entry in db document for user {user.email}")

    return(commons['supabase'].table("users").insert(
        {"user_id": user.id, "email": user.email, "date": date, "requests_count": 1}).execute())

def update_user_request_count(commons: CommonsDep, user:User, date, requests_count):
    logger.info(f"User {user.email} request count updated to {requests_count}")
    commons['supabase'].table("users").update(
        { "requests_count": requests_count}).match({"user_id": user.id, "date": date}).execute()
    
