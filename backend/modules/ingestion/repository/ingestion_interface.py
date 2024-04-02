from abc import ABC, abstractmethod
from typing import List

from modules.ingestion.entity.ingestion import IngestionEntity


class IngestionInterface(ABC):

    @abstractmethod
    def get_all_ingestions(self) -> List[IngestionEntity]:
        """
        Get all the knowledge in a brain
        Args:
            brain_id (UUID): The id of the brain
        """
        pass
