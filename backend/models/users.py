from typing import Optional
from uuid import UUID

from logger import get_logger
from models.databases.supabase.supabase import SupabaseDB
from models.settings import get_supabase_db
from pydantic import BaseModel

logger = get_logger(__name__)


# [TODO] Rename the user table and its references to 'user_usage'
class User(BaseModel):
    id: UUID
    email: Optional[str]
    user_openai_api_key: Optional[str] = None
    requests_count: int = 0

    @property
    def supabase_db(self) -> SupabaseDB:
        return get_supabase_db()

    # [TODO] Rename the user table and its references to 'user_usage'

    def create_user(self, date):
        """
        Create a new user entry in the database

        Args:
            date (str): Date of the request
        """
        logger.info(f"New user entry in db document for user {self.email}")

        return self.supabase_db.create_user(self.id, self.email, date)

    def get_user_request_stats(self):
        """
        Fetch the user request stats from the database
        """
        request = self.supabase_db.get_user_request_stats(self.id)

        return request.data

    def increment_user_request_count(self, date):
        """
        Increment the user request count in the database
        """
        response = self.supabase_db.fetch_user_requests_count(self.id, date)

        userItem = next(iter(response.data or []), {"requests_count": 0})
        requests_count = userItem["requests_count"] + 1
        logger.info(f"User {self.email} request count updated to {requests_count}")
        self.supabase_db.update_user_request_count(self.id, requests_count, date)

        self.requests_count = requests_count
