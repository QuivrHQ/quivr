from logger import get_logger
from models.settings import CommonsDep
from models.users import User

logger = get_logger(__name__)


def create_user(commons: CommonsDep, user: User, date):
    logger.info(f"New user entry in db document for user {user.email}")

    return (
        commons["supabase"]
        .table("users")
        .insert(
            {"user_id": user.id, "email": user.email, "date": date, "requests_count": 1}
        )
        .execute()
    )
