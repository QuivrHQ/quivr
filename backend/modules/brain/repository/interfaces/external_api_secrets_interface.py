from abc import ABC, abstractmethod
from typing import List
from uuid import UUID


# TODO: Replace BrainsVectors with KnowledgeVectors interface instead
class BrainsVectorsInterface(ABC):
    @abstractmethod
    def create_brain_vector(self, brain_id, vector_id, file_sha1):
        """
        Create a brain vector
        """
        pass

    @abstractmethod
    def get_vector_ids_from_file_sha1(self, file_sha1: str):
        """
        Get vector ids from file sha1
        """
        pass

    @abstractmethod
    def get_brain_vector_ids(self, brain_id) -> List[UUID]:
        """
        Get brain vector ids
        """
        pass

    @abstractmethod
    def delete_file_from_brain(self, brain_id, file_name: str):
        """
        Delete file from brain
        """
        pass

    @abstractmethod
    def delete_brain_vector(self, brain_id: str):
        """
        Delete brain vector
        """
        pass
