from quivr_api.logger import get_logger
from quivr_api.models.databases.supabase.supabase import SupabaseDB
from quivr_api.models.settings import PostHogSettings, get_supabase_db
from quivr_api.modules.user.entity.user_identity import UserIdentity

logger = get_logger(__name__)


class UserUsage(UserIdentity):
    daily_requests_count: int = 0

    def __init__(self, **data):
        super().__init__(**data)

    @property
    def supabase_db(self) -> SupabaseDB:
        return get_supabase_db()

    def get_user_daily_usage(self):
        """
        Fetch the user request stats from the database
        """
        request = self.supabase_db.get_user_usage(self.id)
        return request

    def get_models(self):
        """
        Fetch the user request stats from the database
        """
        request = self.supabase_db.get_models()

        return request

    def get_user_settings(self):
        """
        Fetch the user settings from the database
        """
        posthog = PostHogSettings()
        request = self.supabase_db.get_user_settings(self.id)
        if request is not None and request.get("is_premium", False):
            posthog.set_once_user_properties(
                self.id, "HAS_OR_HAD_PREMIUM", {"is_was_premium": "true"}
            )
            posthog.set_user_properties(
                self.id, "CURRENT_PREMIUM", {"is_premium": "true"}
            )
        else:
            posthog.set_user_properties(
                self.id, "CURRENT_PREMIUM", {"is_premium": "false"}
            )

        return request

    def get_user_monthly_usage(self, date):
        """
        Fetch the user monthly usage from the database
        """
        posthog = PostHogSettings()
        request = self.supabase_db.get_user_requests_count_for_month(self.id, date)
        posthog.set_user_properties(
            self.id, "MONTHLY_USAGE", {"monthly_chat_usage": request}
        )

        return request

    def handle_increment_user_request_count(self, date, number=1):
        """
        Increment the user request count in the database
        """
        current_requests_count = self.supabase_db.get_user_requests_count_for_month(
            self.id, date
        )

        daily_requests_count = self.supabase_db.get_user_requests_count_for_day(
            self.id, date
        )

        # BUG: could be a bug, we are assuming that 0 means no records !
        if daily_requests_count == 0:
            logger.info("Request count is 0, creating new record")
            if self.email is None:
                raise ValueError("User Email should be defined for daily usage table")
            self.supabase_db.create_user_daily_usage(
                user_id=self.id, date=date, user_email=self.email, number=number
            )
            self.daily_requests_count = number
            return

        self.supabase_db.increment_user_request_count(
            user_id=self.id,
            date=date,
            number=daily_requests_count + number,
        )

        self.daily_requests_count = current_requests_count + number

        logger.info(
            f"User {self.email} request count updated to {self.daily_requests_count}"
        )
