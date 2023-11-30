from abc import ABC, abstractmethod

from modules.knowledge.dto.inputs import CreateKnowledgeProperties
from modules.knowledge.entity.knowledge import Knowledge


class BrainsInterface(ABC):
    @abstractmethod
    def insert_knowledge(self, knowledge: CreateKnowledgeProperties) -> Knowledge:
        """
        Add a knowledge
        """
        pass
