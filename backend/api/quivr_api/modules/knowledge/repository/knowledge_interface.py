from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from quivr_api.modules.knowledge.dto.inputs import (
    CreateKnowledgeProperties,
    KnowledgeStatus,
)
from quivr_api.modules.knowledge.dto.outputs import DeleteKnowledgeResponse
from quivr_core.models import QuivrKnowledge as Knowledge


class KnowledgeInterface(ABC):
    @abstractmethod
    def insert_knowledge(self, knowledge: CreateKnowledgeProperties) -> Knowledge:
        """
        Add a knowledge
        """
        pass

    @abstractmethod
    def remove_knowledge_by_id(
        # todo: update remove brain endpoints to first delete the knowledge
        self,
        knowledge_id: UUID,
    ) -> DeleteKnowledgeResponse:
        """
        Args:
            knowledge_id (UUID): The id of the knowledge

        Returns:
            str: Status message
        """
        pass

    @abstractmethod
    def get_knowledge_by_id(self, knowledge_id: UUID) -> Knowledge:
        """
        Get a knowledge by its id
        Args:
            brain_id (UUID): The id of the brain
        """
        pass

    @abstractmethod
    def get_all_knowledge_in_brain(self, brain_id: UUID) -> List[Knowledge]:
        """
        Get all the knowledge in a brain
        Args:
            brain_id (UUID): The id of the brain
        """
        pass

    @abstractmethod
    def remove_brain_all_knowledge(self, brain_id: UUID) -> None:
        """
        Remove all knowledge in a brain
        Args:
            brain_id (UUID): The id of the brain
        """
        pass

    @abstractmethod
    def update_status_knowledge(self, knowledge_id: UUID, status: KnowledgeStatus):
        """
        Update the status of a knowledge
        """
        pass
