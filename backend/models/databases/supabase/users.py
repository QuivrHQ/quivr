from models.databases.repository import Repository

from logger import get_logger

logger = get_logger(__name__)


class User(Repository):
    def __init__(self, supabase_client):
        super().__init__(supabase_client)

    # [TODO] Rename the user table and its references to 'user_usage'
    def create_user(self, user_id, user_email, date):
        """
        Create a new user entry in the database

        Args:
            date (str): Date of the request
        """
        logger.info(f"New user entry in db document for user {user_email}")

        return (
            self.db.table("users")
            .insert(
                {
                    "user_id": user_id,
                    "email": user_email,
                    "date": date,
                    "requests_count": 1,
                }
            )
            .execute()
        )

    def get_user_request_stats(self, user_id):
        """
        Fetch the user request stats from the database
        """
        requests_stats = (
            self.db.from_("users")
            .select("*")
            .filter("user_id", "eq", user_id)
            .execute()
        )
        return requests_stats.data

    def fetch_user_requests_count(self, user_id, date):
        """
        Fetch the user request count from the database
        """
        response = (
            self.db.from_("users")
            .select("*")
            .filter("user_id", "eq", user_id)
            .filter("date", "eq", date)
            .execute()
        )
        userItem = next(iter(response.data or []), {"requests_count": 0})

        return userItem["requests_count"]

    def increment_user_request_count(self, date):
        """
        Increment the user request count in the database
        """
        requests_count = self.fetch_user_requests_count(date) + 1
        logger.info(f"User {self.email} request count updated to {requests_count}")
        self.db.table("users").update(
            {"requests_count": requests_count}
        ).match({"user_id": self.id, "date": date}).execute()
        
        return requests_count
