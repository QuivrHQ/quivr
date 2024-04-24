import os
import tempfile
from typing import Any, Optional
from uuid import UUID

from fastapi import UploadFile
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from logger import get_logger
from models.databases.supabase.supabase import SupabaseDB
from models.settings import get_supabase_db
from modules.brain.service.brain_vector_service import BrainVectorService
from packages.files.file import compute_sha1_from_file
from pydantic import BaseModel

logger = get_logger(__name__)


class File(BaseModel):
    id: Optional[UUID] = None
    file: Optional[UploadFile] = None
    file_name: Optional[str] = ""
    file_size: Optional[int] = None
    file_sha1: Optional[str] = ""
    vectors_ids: Optional[list] = []
    file_extension: Optional[str] = ""
    content: Optional[Any] = None
    chunk_size: int = 800
    chunk_overlap: int = 200
    documents: Optional[Document] = None

    @property
    def supabase_db(self) -> SupabaseDB:
        return get_supabase_db()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.file:
            self.file_name = self.file.filename
            self.file_size = self.file.size  # pyright: ignore reportPrivateUsage=none
            self.file_extension = os.path.splitext(
                self.file.filename  # pyright: ignore reportPrivateUsage=none
            )[-1].lower()

    async def compute_file_sha1(self):
        """
        Compute the sha1 of the file using a temporary file
        """
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=self.file.filename,  # pyright: ignore reportPrivateUsage=none
        ) as tmp_file:
            await self.file.seek(0)  # pyright: ignore reportPrivateUsage=none
            self.content = (
                await self.file.read()  # pyright: ignore reportPrivateUsage=none
            )
            tmp_file.write(self.content)
            tmp_file.flush()
            self.file_sha1 = compute_sha1_from_file(tmp_file.name)

        os.remove(tmp_file.name)

    def compute_documents(self, loader_class):
        """
        Compute the documents from the file

        Args:
            loader_class (class): The class of the loader to use to load the file
        """
        logger.info(f"Computing documents from file {self.file_name}")

        documents = []
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=self.file.filename,  # pyright: ignore reportPrivateUsage=none
        ) as tmp_file:
            tmp_file.write(self.content)  # pyright: ignore reportPrivateUsage=none
            tmp_file.flush()
            loader = loader_class(tmp_file.name)
            documents = loader.load()

        os.remove(tmp_file.name)

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
            brain_id, self.file_sha1  # type: ignore
        )

        if len(response.data) == 0:
            return False

        return True

    def file_is_empty(self):
        """
        Check if file is empty by checking if the file pointer is at the beginning of the file
        """
        return self.file.size < 1  # pyright: ignore reportPrivateUsage=none

    def link_file_to_brain(self, brain_id):
        self.set_file_vectors_ids()

        if self.vectors_ids is None:
            return

        brain_vector_service = BrainVectorService(brain_id)

        for vector_id in self.vectors_ids:  # pyright: ignore reportPrivateUsage=none
            brain_vector_service.create_brain_vector(vector_id["id"], self.file_sha1)
