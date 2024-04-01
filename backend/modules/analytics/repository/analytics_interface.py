from abc import ABC, abstractmethod
from uuid import UUID
from modules.analytics.entity.analytics import BrainsUsages

class AnalyticsInterface(ABC):
    @abstractmethod
    def get_brains_usages(self, user_id: UUID) -> BrainsUsages:
        """
        Get user brains usage
        Args:
            user_id (UUID): The id of the user
        """
        pass