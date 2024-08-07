from uuid import UUID

from quivr_api.logger import get_logger
from quivr_api.modules.brain.repository.brains_vectors import BrainsVectors
from quivr_api.modules.knowledge.repository.storage import Storage

logger = get_logger(__name__)


class BrainVectorService:
    def __init__(self, brain_id: UUID):
        self.repository = BrainsVectors()
        self.brain_id = brain_id
        self.storage = Storage()

    def create_brain_vector(self, vector_id: str, file_sha1: str):
        return self.repository.create_brain_vector(self.brain_id, vector_id, file_sha1)  # type: ignore

    def update_brain_with_file(self, file_sha1: str):
        # not  used
        vector_ids = self.repository.get_vector_ids_from_file_sha1(file_sha1)
        if vector_ids is None or len(vector_ids) == 0:
            logger.info(f"No vector ids found for file {file_sha1}")
            return

        for vector_id in vector_ids:
            self.create_brain_vector(vector_id, file_sha1)

    def delete_file_from_brain(self, file_name: str, only_vectors: bool = False):
        file_name_with_brain_id = f"{self.brain_id}/{file_name}"
        if not only_vectors:
            self.storage.remove_file(file_name_with_brain_id)
        return self.repository.delete_file_from_brain(self.brain_id, file_name)  # type: ignore

    def delete_file_url_from_brain(self, file_name: str):
        return self.repository.delete_file_from_brain(self.brain_id, file_name)  # type: ignore

    @property
    def brain_size(self):
        return self.repository.get_brain_size(self.brain_id)
