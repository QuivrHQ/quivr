from typing import Any, List
from uuid import UUID

from logger import get_logger
from modules.brain.repository.brains_vectors import BrainsVectors
from modules.brain.repository.interfaces.brains_vectors_interface import (
    BrainsVectorsInterface,
)
from modules.knowledge.repository.storage import Storage
from packages.embeddings.vectors import get_unique_files_from_vector_ids

logger = get_logger(__name__)


class BrainVectorService:
    repository: BrainsVectorsInterface
    id: UUID
    files: List[Any] = []

    def __init__(self, brain_id: UUID):
        self.repository = BrainsVectors()
        self.id = brain_id

    def create_brain_vector(self, vector_id, file_sha1):
        return self.repository.create_brain_vector(self.id, vector_id, file_sha1)  # type: ignore

    def update_brain_with_file(self, file_sha1: str):
        # not  used
        vector_ids = self.repository.get_vector_ids_from_file_sha1(file_sha1)
        if vector_ids == None or len(vector_ids) == 0:
            logger.info(f"No vector ids found for file {file_sha1}")
            return

        for vector_id in vector_ids:
            self.create_brain_vector(vector_id, file_sha1)

    def get_unique_brain_files(self):
        """
        Retrieve unique brain data (i.e. uploaded files and crawled websites).
        """

        vector_ids = self.repository.get_brain_vector_ids(self.id)  # type: ignore
        self.files = get_unique_files_from_vector_ids(vector_ids)

        return self.files

    def delete_file_from_brain(self, file_name: str):
        file_name_with_brain_id = f"{self.id}/{file_name}"
        storage = Storage()
        storage.remove_file(file_name_with_brain_id)
        return self.repository.delete_file_from_brain(self.id, file_name)  # type: ignore

    def delete_file_url_from_brain(self, file_name: str):
        return self.repository.delete_file_from_brain(self.id, file_name)  # type: ignore

    @property
    def brain_size(self):
        # TODO: change the calculation of the brain size, calculate the size stored for the embeddings + what's in the storage
        self.get_unique_brain_files()
        current_brain_size = sum(float(doc["size"]) for doc in self.files)

        return current_brain_size
