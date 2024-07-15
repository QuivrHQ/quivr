from pathlib import Path
from typing import List, Optional

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from pydantic import BaseModel

from quivr_api.logger import get_logger
from quivr_api.models.databases.supabase.supabase import SupabaseDB
from quivr_api.models.settings import get_supabase_db
from quivr_api.modules.brain.service.brain_vector_service import BrainVectorService
from quivr_api.packages.files.file import compute_sha1_from_content

logger = get_logger(__name__)


class File(BaseModel):
    file_name: str
    tmp_file_path: Path
    bytes_content: bytes
    file_size: int
    file_extension: str
    chunk_size: int = 400
    chunk_overlap: int = 100
    documents: List[Document] = []
    file_sha1: Optional[str] = None
    vectors_ids: Optional[list] = []

    def __init__(self, **data):
        super().__init__(**data)
        data["file_sha1"] = compute_sha1_from_content(data["bytes_content"])

    @property
    def supabase_db(self) -> SupabaseDB:
        return get_supabase_db()

    def compute_documents(self, loader_class):
        """
        Compute the documents from the file

        Args:
            loader_class (class): The class of the loader to use to load the file
        """
        logger.info(f"Computing documents from file {self.file_name}")
        loader = loader_class(self.tmp_file_path)
        loaded_content = loader.load()
        documents = (
            [loaded_content] if not isinstance(loaded_content, list) else loaded_content
        )

        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )

        self.documents = text_splitter.split_documents(documents)

    def set_file_vectors_ids(self):
        """
        Set the vectors_ids property with the ids of the vectors
        that are associated with the file in the vectors table
        """
        self.vectors_ids = self.supabase_db.get_vectors_by_file_sha1(
            self.file_sha1
        ).data

    def file_already_exists(self):
        """
        Check if file already exists in vectors table
        """
        self.set_file_vectors_ids()

        # if the file does not exist in vectors then no need to go check in brains_vectors
        if len(self.vectors_ids) == 0:  # pyright: ignore reportPrivateUsage=none
            return False

        return True

    def file_already_exists_in_brain(self, brain_id):
        """
        Check if file already exists in a brain

        Args:
            brain_id (str): Brain id
        """
        response = self.supabase_db.get_brain_vectors_by_brain_id_and_file_sha1(
            brain_id,
            self.file_sha1,  # type: ignore
        )

        if len(response.data) == 0:
            return False

        return True

    def file_is_empty(self):
        """
        Check if file is empty by checking if the file pointer is at the beginning of the file
        """
        return self.file_size < 1  # pyright: ignore reportPrivateUsage=none

    def link_file_to_brain(self, brain_id):
        self.set_file_vectors_ids()

        if self.vectors_ids is None:
            return

        brain_vector_service = BrainVectorService(brain_id)

        for vector_id in self.vectors_ids:  # pyright: ignore reportPrivateUsage=none
            brain_vector_service.create_brain_vector(vector_id["id"], self.file_sha1)
