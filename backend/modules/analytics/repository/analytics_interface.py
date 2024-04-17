from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from modules.analytics.entity.analytics import BrainsUsages, Range

class AnalyticsInterface(ABC):
    @abstractmethod
    def get_brains_usages(self, user_id: UUID, graph_range: Range = Range.WEEK, brain_id: Optional[UUID] = None) -> BrainsUsages:
        """
        Get user brains usage
        Args:
            user_id (UUID): The id of the user
            brain_id (Optional[UUID]): The id of the brain, optional
        """
        pass