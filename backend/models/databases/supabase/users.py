from models.databases.repository import Repository

from logger import get_logger

logger = get_logger(__name__)


class User(Repository):
    def __init__(self, supabase_client):
        self.db = supabase_client

    # [TODO] Rename the user table and its references to 'user_usage'
    def create_user(self, user_id, user_email, date):
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
        return requests_stats

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

        return response

    def update_user_request_count(self, user_id, requests_count, date):
        response = (
            self.db.table("users")
            .update({"requests_count": requests_count})
            .match({"user_id": user_id, "date": date})
            .execute()
        )

        return response

    def get_user_email(self, user_id):
        """
        Fetch the user email from the database
        """
        response = (
            self.db.from_("users")
            .select("email")
            .filter("user_id", "eq", user_id)
            .execute()
        )

        return response

    def get_user_stats(self, user_email, date):
        response = (
            self.db.from_("users")
            .select("*")
            .filter("email", "eq", user_email)
            .filter("date", "eq", date)
            .execute()
        )

        return response
