from uuid import UUID

from logger import get_logger
from modules.knowledge.dto.inputs import CreateKnowledgeProperties
from modules.knowledge.entity.knowledge import Knowledge
from modules.knowledge.repository.knowledge_interface import KnowledgeInterface
from modules.knowledge.repository.knowledges import Knowledges

logger = get_logger(__name__)


class KnowledgeService:
    repository: KnowledgeInterface

    def __init__(self):
        self.repository = Knowledges()

    def add_knowledge(self, knowledge_to_add: CreateKnowledgeProperties):
        knowledge = self.repository.insert_knowledge(knowledge_to_add)

        return knowledge

    def get_all_knowledge(self, brain_id: UUID):
        knowledges = self.repository.get_all_knowledge_in_brain(brain_id)

        return knowledges

    def get_knowledge(self, knowledge_id: UUID) -> Knowledge:
        knowledge = self.repository.get_knowledge_by_id(knowledge_id)

        return knowledge

    def remove_brain_all_knowledge(self, brain_id: UUID) -> None:
        self.repository.remove_brain_all_knowledge(brain_id)

        logger.info(
            f"All knowledge in brain {brain_id} removed successfully from table"
        )

    def remove_knowledge(self, knowledge_id: UUID):
        message = self.repository.remove_knowledge_by_id(knowledge_id)

        return message
