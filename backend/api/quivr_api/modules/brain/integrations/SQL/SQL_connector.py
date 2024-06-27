from quivr_api.logger import get_logger
from quivr_api.modules.brain.entity.integration_brain import IntegrationEntity
from quivr_api.modules.brain.repository.integration_brains import IntegrationBrain
from quivr_api.modules.knowledge.repository.knowledge_interface import (
    KnowledgeInterface,
)
from quivr_api.modules.knowledge.service.knowledge_service import KnowledgeService

logger = get_logger(__name__)


class SQLConnector(IntegrationBrain):
    """A class to interact with an SQL database"""

    credentials: dict[str, str] = None
    integration_details: IntegrationEntity = None
    brain_id: str = None
    user_id: str = None
    knowledge_service: KnowledgeInterface

    def __init__(self, brain_id: str, user_id: str):
        super().__init__()
        self.brain_id = brain_id
        self.user_id = user_id
        self._load_credentials()
        self.knowledge_service = KnowledgeService()

    def _load_credentials(self) -> dict[str, str]:
        """Load the Notion credentials"""
        self.integration_details = self.get_integration_brain(self.brain_id)
        if self.credentials is None:
            logger.info("Loading Notion credentials")
            self.integration_details.credentials = {
                "uri": self.integration_details.settings.get("uri", "")
            }
            self.update_integration_brain(
                self.brain_id, self.user_id, self.integration_details
            )
            self.credentials = self.integration_details.credentials
        else:  # pragma: no cover
            self.credentials = self.integration_details.credentials
