from collections import defaultdict
from datetime import datetime, timedelta
from uuid import UUID
from models.settings import get_supabase_client
from modules.analytics.entity.analytics import BrainsUsages, BrainUsages, Usage
from modules.analytics.repository.analytics_interface import AnalyticsInterface
from modules.brain.service.brain_user_service import BrainUserService

brain_user_service = BrainUserService()

class Analytics(AnalyticsInterface):
    def __init__(self):
        supabase_client = get_supabase_client()
        self.db = supabase_client

    def get_brains_usages(self, user_id: UUID) -> BrainsUsages:
        user_brains = brain_user_service.get_user_brains(user_id)
        brains_usages = []

        for brain in user_brains:
            chat_history = (
                self.db.from_("chat_history")
                .select("*")
                .filter("brain_id", "eq", str(brain.id))
                .execute()
            ).data

            usage_per_day = defaultdict(int)
            for chat in chat_history:
                message_time = datetime.strptime(chat['message_time'], "%Y-%m-%dT%H:%M:%S.%f")
                usage_per_day[message_time.date()] += 1

            # Generate all dates in the last 7 days
            start_date = datetime.now().date() - timedelta(days=7)
            all_dates = [start_date + timedelta(days=i) for i in range(7)]
            for date in all_dates:
                usage_per_day[date] += 0

            usages = [Usage(date=date, usage_count=count) for date, count in usage_per_day.items() if start_date <= date <= datetime.now().date()]
            brain_usages = BrainUsages(brain_id=brain.id, usages=usages)
            brains_usages.append(brain_usages)

        return BrainsUsages(brains_usages=brains_usages)