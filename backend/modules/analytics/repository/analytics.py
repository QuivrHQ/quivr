from collections import defaultdict
from uuid import UUID

from modules.analytics.entity.analytics import BrainsUsages
from modules.analytics.entity.analytics import BrainUsage
from modules.brain.service.brain_user_service import BrainUserService

brain_user_service = BrainUserService()

def get_brains_usages(self, user_id: UUID) -> BrainsUsages:
    """
    Get user brains usage
    Args:
        user_id (UUID): The id of the user
    """

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
            usage_per_day[chat.message_time.date()] += 1

        brain_usages = [BrainUsage(date=date, usage_count=count) for date, count in usage_per_day.items()]
        brains_usages.append(BrainsUsages(brain_id=brain.id, usages=brain_usages))

    return BrainsUsages(brains_usages=brains_usages)