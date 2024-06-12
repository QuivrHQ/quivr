from datetime import datetime, timedelta
from uuid import UUID

from logger import get_logger
from models.databases.repository import Repository

logger = get_logger(__name__)


# TODO: change the name of this class because another one already exists
class UserUsage(Repository):
    def __init__(self, supabase_client):
        self.db = supabase_client

    def create_user_daily_usage(
        self, user_id: UUID, user_email: str, date: datetime, number: int = 1
    ):
        return (
            self.db.table("user_daily_usage")
            .insert(
                {
                    "user_id": str(user_id),
                    "email": user_email,
                    "date": date,
                    "daily_requests_count": number,
                }
            )
            .execute()
        )

    def get_user_settings(self, user_id):
        """
        Fetch the user settings from the database
        """

        user_settings_response = (
            self.db.from_("user_settings")
            .select("*")
            .filter("user_id", "eq", str(user_id))
            .execute()
        ).data

        if len(user_settings_response) == 0:
            # Create the user settings
            user_settings_response = (
                self.db.table("user_settings")
                .insert({"user_id": str(user_id)})
                .execute()
            ).data

        if len(user_settings_response) == 0:
            raise ValueError("User settings could not be created")

        user_settings = user_settings_response[0]

        return user_settings

    def get_model_settings(self):
        """
        Fetch the user settings from the database
        """

        model_settings_response = (self.db.from_("models").select("*").execute()).data

        if len(model_settings_response) == 0:
            raise ValueError("An issue occured while fetching the model settings")

        return model_settings_response

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
        return 0

    def get_user_requests_count_for_month(self, user_id, date):
        """
        Fetch the user request count from the database
        """
        date_30_days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y%m%d")

        response = (
            self.db.from_("user_daily_usage")
            .select("daily_requests_count")
            .filter("user_id", "eq", user_id)
            .filter("date", "gte", date_30_days_ago)
            .execute()
        ).data

        if response and len(response) > 0:
            return sum(row["daily_requests_count"] for row in response)
        return 0

    def increment_user_request_count(self, user_id, date, number: int = 1):
        """
        Increment the user's requests count for a specific day
        """

        self.update_user_request_count(user_id, daily_requests_count=number, date=date)

    def update_user_request_count(self, user_id, daily_requests_count, date):
        response = (
            self.db.table("user_daily_usage")
            .update({"daily_requests_count": daily_requests_count})
            .match({"user_id": user_id, "date": date})
            .execute()
        )

        return response
