from typing import Any, List, Optional
from uuid import UUID

from logger import get_logger
from models.databases.supabase.supabase import SupabaseDB
from models.settings import get_supabase_client, get_supabase_db
from packages.embeddings.vectors import get_unique_files_from_vector_ids
from pydantic import BaseModel
from supabase.client import Client

logger = get_logger(__name__)


class Brain(BaseModel):
    id: Optional[UUID] = None
    name: Optional[str] = "Default brain"
    description: Optional[str] = "This is a description"
    status: Optional[str] = "private"
    model: Optional[str] = None
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = 256
    files: List[Any] = []
    prompt_id: Optional[UUID] = None

    class Config:
        arbitrary_types_allowed = True

    @property
    def supabase_client(self) -> Client:
        return get_supabase_client()

    @property
    def supabase_db(self) -> SupabaseDB:
        return get_supabase_db()

    @property
    def brain_size(self):
        self.get_unique_brain_files()
        current_brain_size = sum(float(doc["size"]) for doc in self.files)

        return current_brain_size

    @classmethod
    def create(cls, *args, **kwargs):
        commons = {"supabase": get_supabase_client()}
        return cls(
            commons=commons, *args, **kwargs  # pyright: ignore reportPrivateUsage=none
        )  # pyright: ignore reportPrivateUsage=none

    def create_brain_vector(self, vector_id, file_sha1):
        return self.supabase_db.create_brain_vector(self.id, vector_id, file_sha1)  # type: ignore

    def get_vector_ids_from_file_sha1(self, file_sha1: str):
        return self.supabase_db.get_vector_ids_from_file_sha1(file_sha1)

    def update_brain_with_file(self, file_sha1: str):
        # not  used
        vector_ids = self.get_vector_ids_from_file_sha1(file_sha1)
        for vector_id in vector_ids:
            self.create_brain_vector(vector_id, file_sha1)

    def get_unique_brain_files(self):
        """
        Retrieve unique brain data (i.e. uploaded files and crawled websites).
        """

        vector_ids = self.supabase_db.get_brain_vector_ids(self.id)  # type: ignore
        self.files = get_unique_files_from_vector_ids(vector_ids)

        return self.files

    def delete_file_from_brain(self, file_name: str):
        file_name_with_brain_id = f"{self.id}/{file_name}"
        self.supabase_client.storage.from_("quivr").remove([file_name_with_brain_id])
        return self.supabase_db.delete_file_from_brain(self.id, file_name)  # type: ignore

    def get_all_knowledge_in_brain(self):
        """
        Retrieve unique brain data (i.e. uploaded files and crawled websites).
        """

        vector_ids = self.supabase_db.get_brain_vector_ids(self.id)  # type: ignore
        self.files = get_unique_files_from_vector_ids(vector_ids)

        return self.files
