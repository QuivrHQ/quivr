from logger import get_logger
from models.databases.supabase.supabase import SupabaseDB
from models.settings import get_supabase_db
from modules.user.entity.user_identity import UserIdentity

logger = get_logger(__name__)


class UserUsage(UserIdentity):
    daily_requests_count: int = 0

    def __init__(self, **data):
        super().__init__(**data)

    @property
    def supabase_db(self) -> SupabaseDB:
        return get_supabase_db()

    def get_user_usage(self):
        """
        Fetch the user request stats from the database
        """
        request = self.supabase_db.get_user_usage(self.id)

        return request

    def get_user_settings(self):
        """
        Fetch the user settings from the database
        """
        request = self.supabase_db.get_user_settings(self.id)

        return request

    def handle_increment_user_request_count(self, date):
        """
        Increment the user request count in the database
        """
        current_requests_count = self.supabase_db.get_user_requests_count_for_day(
            self.id, date
        )

        if current_requests_count is None:
            if self.email is None:
                raise ValueError("User Email should be defined for daily usage table")
            self.supabase_db.create_user_daily_usage(
                user_id=self.id, date=date, user_email=self.email
            )
            self.daily_requests_count = 1
            return

        self.supabase_db.increment_user_request_count(
            user_id=self.id,
            date=date,
            current_requests_count=current_requests_count,
        )

        self.daily_requests_count = current_requests_count

        logger.info(
            f"User {self.email} request count updated to {current_requests_count}"
        )
