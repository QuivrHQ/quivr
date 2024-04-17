from collections import defaultdict
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from models.settings import get_supabase_client
from modules.analytics.entity.analytics import BrainsUsages, Range, Usage
from modules.brain.service.brain_user_service import BrainUserService

brain_user_service = BrainUserService()


class Analytics:
    def __init__(self):
        supabase_client = get_supabase_client()
        self.db = supabase_client

    def get_brains_usages(
        self, user_id: UUID, graph_range: Range, brain_id: Optional[UUID] = None
    ) -> BrainsUsages:
        user_brains = brain_user_service.get_user_brains(user_id)
        if brain_id is not None:
            user_brains = [brain for brain in user_brains if brain.id == brain_id]

        usage_per_day = defaultdict(int)

        brain_ids = [brain.id for brain in user_brains]
        chat_history = (
            self.db.from_("chat_history")
            .select("*")
            .in_("brain_id", brain_ids)
            .execute()
        ).data

        for chat in chat_history:
            message_time = datetime.strptime(
                chat["message_time"], "%Y-%m-%dT%H:%M:%S.%f"
            )
            usage_per_day[message_time.date()] += 1

        start_date = datetime.now().date() - timedelta(days=graph_range)
        all_dates = [start_date + timedelta(days=i) for i in range(graph_range)]

        for date in all_dates:
            usage_per_day[date] += 0

        usages = sorted(
            [
                Usage(date=date, usage_count=count)
                for date, count in usage_per_day.items()
                if start_date <= date <= datetime.now().date()
            ],
            key=lambda usage: usage.date,
        )

        return BrainsUsages(usages=usages)
