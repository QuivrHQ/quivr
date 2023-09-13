from datetime import datetime
from uuid import UUID

from logger import get_logger
from models.databases.repository import Repository

logger = get_logger(__name__)


class UserUsage(Repository):
    def __init__(self, supabase_client):
        self.db = supabase_client

    def create_user_daily_usage(self, user_id: UUID, user_email: str, date: datetime):
        return (
            self.db.table("user_daily_usage")
            .insert(
                {
                    "user_id": str(user_id),
                    "email": user_email,
                    "date": date,
                    "daily_requests_count": 1,
                }
            )
            .execute()
        )

    def get_user_settings(self, user_id):
        """
        Fetch the user settings from the database
        """
        response = (
            self.db.from_("user_settings")
            .select("*")
            .filter("user_id", "eq", str(user_id))
            .execute()
        ).data

        if len(response) == 0:
            # Create the user settings
            result = (
                self.db.table("user_settings")
                .insert({"user_id": str(user_id)})
                .execute()
            )
            if result:
                return self.get_user_settings(user_id)
            else:
                raise ValueError("User settings could not be created")
        if response and len(response) > 0:
            return response[0]
        return None

    def get_user_usage(self, user_id):
        """
        Fetch the user request stats from the database
        """
        requests_stats = (
            self.db.from_("user_daily_usage")
            .select("*")
            .filter("user_id", "eq", user_id)
            .execute()
        )
        return requests_stats.data

    def get_user_requests_count_for_day(self, user_id, date):
        """
        Fetch the user request count from the database
        """
        response = (
            self.db.from_("user_daily_usage")
            .select("daily_requests_count")
            .filter("user_id", "eq", user_id)
            .filter("date", "eq", date)
            .execute()
        ).data

        if response and len(response) > 0:
            return response[0]["daily_requests_count"]
        return None

    def increment_user_request_count(self, user_id, date, current_requests_count: int):
        """
        Increment the user's requests count for a specific day
        """

        self.update_user_request_count(
            user_id, daily_requests_count=current_requests_count + 1, date=date
        )

    def update_user_request_count(self, user_id, daily_requests_count, date):
        response = (
            self.db.table("user_daily_usage")
            .update({"daily_requests_count": daily_requests_count})
            .match({"user_id": user_id, "date": date})
            .execute()
        )

        return response

    def get_user_email(self, user_id):
        """
        Fetch the user email from the database
        """
        response = (
            self.db.from_("user_daily_usage")
            .select("email")
            .filter("user_id", "eq", user_id)
            .execute()
        ).data

        if response and len(response) > 0:
            return response[0]["email"]
        return None
