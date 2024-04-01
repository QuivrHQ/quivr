from abc import abstractmethod
from uuid import UUID

from modules.analytics.entity.analytics import BrainsUsage

@abstractmethod
def get_brains_usage(self, user_id: UUID) -> BrainsUsage:
    """
    Get user brains usage
    Args:
        user_id (UUID): The id of the user
    """
    pass