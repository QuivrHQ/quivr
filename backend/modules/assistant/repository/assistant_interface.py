from abc import ABC, abstractmethod
from typing import List

from modules.assistant.entity.assistant import AssistantEntity


class AssistantInterface(ABC):

    @abstractmethod
    def get_all_assistants(self) -> List[AssistantEntity]:
        """
        Get all the knowledge in a brain
        Args:
            brain_id (UUID): The id of the brain
        """
        pass
