from datetime import datetime

from fastapi import HTTPException
from models.settings import get_supabase_db
from models.user_identity import UserIdentity
from pydantic import DateError


async def verify_api_key(
    api_key: str,
) -> bool:
    try:
        # Use UTC time to avoid timezone issues
        current_date = datetime.utcnow().date()
        supabase_db = get_supabase_db()
        result = supabase_db.get_active_api_key(api_key)

        if result.data is not None and len(result.data) > 0:
            api_key_creation_date = datetime.strptime(
                result.data[0]["creation_time"], "%Y-%m-%dT%H:%M:%S"
            ).date()

            if (api_key_creation_date.month == current_date.month) and (
                api_key_creation_date.year == current_date.year
            ):
                return True
        return False
    except DateError:
        return False


async def get_user_from_api_key(
    api_key: str,
) -> UserIdentity:
    supabase_db = get_supabase_db()

    user_id_data = supabase_db.get_user_id_by_api_key(api_key)

    if not user_id_data.data:
        raise HTTPException(status_code=400, detail="Invalid API key.")

    user_id = user_id_data.data[0]["user_id"]

    email = supabase_db.get_user_email(user_id)

    return UserIdentity(email=email, id=user_id)
