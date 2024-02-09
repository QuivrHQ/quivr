import os
import tempfile
from io import BytesIO

from fastapi import UploadFile
from logger import get_logger
from modules.brain.entity.integration_brain import IntegrationEntity
from modules.brain.repository.integration_brains import IntegrationBrain
from modules.knowledge.dto.inputs import CreateKnowledgeProperties
from modules.knowledge.repository.knowledge_interface import KnowledgeInterface
from modules.knowledge.service.knowledge_service import KnowledgeService
from repository.files.upload_file import upload_file_storage

logger = get_logger(__name__)


class ExcelConnector(IntegrationBrain):
    """A class to interact with the Notion API"""

    credentials: dict[str, str] = None
    integration_details: IntegrationEntity = None
    brain_id: str = None
    user_id: str = None
    knowledge_service: KnowledgeInterface
    recursive_index_enabled: bool = False
    max_pages: int = 100

    def __init__(self, brain_id: str, user_id: str):
        super().__init__()
        self.brain_id = brain_id
        self.user_id = user_id
        self._load_credentials()
        self.knowledge_service = KnowledgeService()

    def _load_credentials(self) -> dict[str, str]:
        pass

    def upload_file()


if __name__ == "__main__":
    pass
