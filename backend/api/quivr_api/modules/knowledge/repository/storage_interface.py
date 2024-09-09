from abc import ABC, abstractmethod
from io import BufferedReader, FileIO

from quivr_api.modules.knowledge.entity.knowledge import KnowledgeDB


class StorageInterface(ABC):
    @abstractmethod
    async def upload_file_storage(
        self,
        knowledge: KnowledgeDB,
        knowledge_data: FileIO | BufferedReader | bytes,
        upsert: bool = False,
    ):
        pass

    @abstractmethod
    async def remove_file(self, storage_path: str):
        pass
