from typing import Any, List, Optional
from uuid import UUID

from logger import get_logger
from models.databases.supabase.supabase import SupabaseDB
from models.settings import BrainRateLimiting, get_supabase_client, get_supabase_db
from pydantic import BaseModel
from supabase.client import Client
from utils.vectors import get_unique_files_from_vector_ids

logger = get_logger(__name__)


class Brain(BaseModel):
    id: Optional[UUID] = None
    name: Optional[str] = "Default brain"
    description: Optional[str] = "This is a description"
    status: Optional[str] = "private"
    model: Optional[str] = "gpt-3.5-turbo-0613"
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = 256
    openai_api_key: Optional[str] = None
    files: List[Any] = []
    max_brain_size = BrainRateLimiting().max_brain_size
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

    @property
    def remaining_brain_size(self):
        return (
            float(self.max_brain_size)  # pyright: ignore reportPrivateUsage=none
            - self.brain_size  # pyright: ignore reportPrivateUsage=none
        )

    @classmethod
    def create(cls, *args, **kwargs):
        commons = {"supabase": get_supabase_client()}
        return cls(
            commons=commons, *args, **kwargs  # pyright: ignore reportPrivateUsage=none
        )  # pyright: ignore reportPrivateUsage=none

    # TODO: move this to a brand new BrainService
    def get_brain_users(self):
        response = (
            self.supabase_client.table("brains_users")
            .select("id:brain_id, *")
            .filter("brain_id", "eq", self.id)
            .execute()
        )
        return response.data

    # TODO: move this to a brand new BrainService
    def delete_user_from_brain(self, user_id):
        results = (
            self.supabase_client.table("brains_users")
            .select("*")
            .match({"brain_id": self.id, "user_id": user_id})
            .execute()
        )

        if len(results.data) != 0:
            self.supabase_client.table("brains_users").delete().match(
                {"brain_id": self.id, "user_id": user_id}
            ).execute()

    def delete_brain(self, user_id):
        results = self.supabase_db.delete_brain_user_by_id(user_id, self.id)

        if len(results.data) == 0:
            return {"message": "You are not the owner of this brain."}
        else:
            self.supabase_db.delete_brain_vector(self.id)
            self.supabase_db.delete_brain_user(self.id)
            self.supabase_db.delete_brain(self.id)

    def create_brain_vector(self, vector_id, file_sha1):
        return self.supabase_db.create_brain_vector(self.id, vector_id, file_sha1)

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

        vector_ids = self.supabase_db.get_brain_vector_ids(self.id)
        self.files = get_unique_files_from_vector_ids(vector_ids)

        return self.files

    def delete_file_from_brain(self, file_name: str):
        return self.supabase_db.delete_file_from_brain(self.id, file_name)
