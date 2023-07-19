from typing import Optional
from uuid import UUID

from logger import get_logger
from models.settings import common_dependencies, CommonsDep
from pydantic import BaseModel

logger = get_logger(__name__)


class User(BaseModel):
    id: UUID
    email: Optional[str]
    user_openai_api_key: Optional[str] = None
    requests_count: int = 0

    @property
    def commons(self) -> CommonsDep:
        return common_dependencies()

    # [TODO] Rename the user table and its references to 'user_usage'
    def create_user(self, date):
        """
        Create a new user entry in the database

        Args:
            date (str): Date of the request
        """
        logger.info(f"New user entry in db document for user {self.email}")

        return self.commons["db"].create_user(self.id, self.email, date)

    def get_user_request_stats(self):
        """
        Fetch the user request stats from the database
        """
        return self.commons["db"].get_user_request_stats(self.id)

    def fetch_user_requests_count(self, date):
        """
        Fetch the user request count from the database
        """
        return self.commons["db"].fetch_user_requests_count(self.id, date)

    def increment_user_request_count(self, date):
        """
        Increment the user request count in the database
        """
        self.requests_count = self.commons["db"].increment_user_request_count(date)
