import time
from uuid import UUID

from fastapi import HTTPException
from models import UserUsage
from modules.user.entity.user_identity import UserIdentity


class NullableUUID(UUID):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v) -> UUID | None:
        if v == "":
            return None
        try:
            return UUID(v)
        except ValueError:
            return None


def check_user_requests_limit(
    user: UserIdentity,
):
    userDailyUsage = UserUsage(id=user.id, email=user.email)

    userSettings = userDailyUsage.get_user_settings()

    date = time.strftime("%Y%m%d")
    userDailyUsage.handle_increment_user_request_count(date)

    daily_chat_credit = userSettings.get("daily_chat_credit", 0)
    if int(userDailyUsage.daily_requests_count) >= int(daily_chat_credit):
        raise HTTPException(
            status_code=429,  # pyright: ignore reportPrivateUsage=none
            detail="You have reached the maximum number of requests for today.",  # pyright: ignore reportPrivateUsage=none
        )
    else:
        pass
