from uuid import UUID

from logger import get_logger
from models.settings import common_dependencies
from pydantic import BaseModel

logger = get_logger(__name__)
class User(BaseModel):
    id: UUID
    email: str
    user_openai_api_key: str = None
    requests_count: int = 0
    user_openai_api_key: str = None




    def get_user_request_stats(self):
        commons = common_dependencies()
        requests_stats = commons['supabase'].from_('users').select(
            '*').filter("user_id", "eq", self.id).execute()
        return requests_stats.data

    def fetch_user_requests_count(self, date):
        commons = common_dependencies()
        response = (
            commons["supabase"]
            .from_("users")
            .select("*")
            .filter("user_id", "eq", self.id)
            .filter("date", "eq", date)
            .execute()
        )
        userItem = next(iter(response.data or []), {"requests_count": 0})

        return userItem["requests_count"]


    def increment_user_request_count(self, date):
        commons = common_dependencies()
        requests_count = self.fetch_user_requests_count(date) + 1
        logger.info(f"User {self.email} request count updated to {requests_count}")
        commons['supabase'].table("users").update(
            { "requests_count": requests_count}).match({"user_id": self.id, "date": date}).execute()
        self.requests_count = requests_count
        