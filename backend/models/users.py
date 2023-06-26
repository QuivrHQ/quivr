from uuid import UUID

from models.settings import common_dependencies
from pydantic import BaseModel


class User(BaseModel):
    id: UUID
    email: str


    def get_user_request_stats(self):
        commons = common_dependencies()
        requests_stats = commons['supabase'].from_('users').select(
            '*').filter("user_id", "eq", self.id).execute()
        return requests_stats.data


