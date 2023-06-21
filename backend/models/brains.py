import os
from typing import Optional
from uuid import UUID

from models.settings import CommonsDep, common_dependencies
from pydantic import BaseModel


class Brain(BaseModel):
    brain_id: Optional[UUID] = None
    name: str = "New Brain"
    status: Optional[str]= "public"
    model: Optional[str] = "gpt-3.5-turbo-0613"
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = 256
    brain_size: Optional[float] = 0.0
    max_brain_size: Optional[int] = int(os.getenv("MAX_BRAIN_SIZE", 0))
    
class BrainToUpdate(BaseModel): 
    brain_id: UUID
    name: Optional[str] = "New Brain"
    status: Optional[str] = "public"
    model: Optional[str] = "gpt-3.5-turbo-0613"
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = 256
    file_sha1: Optional[str] = ""
    _commons: Optional[CommonsDep] = None

    class Config:
        arbitrary_types_allowed = True

    @property
    def commons(self) -> CommonsDep:
        if not self._commons:
            self.__class__._commons = common_dependencies()
        return self._commons

    @property
    def brain_size(self):
        unique_files = self.get_unique_brain_files()
        current_brain_size = sum(float(doc['size']) for doc in unique_files)

        print('current_brain_size', current_brain_size)
        return current_brain_size

    # To keep ??
    @property
    def brain_filling(self):
        if self.max_brain_size == 0:
            return 0
        return self.brain_size / self.max_brain_size

    @property
    def remaining_brain_size(self):
        return float(self.max_brain_size) - self.brain_size


    @classmethod
    def create(cls, *args, **kwargs):
        commons = common_dependencies()
        return cls(commons=commons, *args, **kwargs)

    def get_user_brains(self, user_id):
        response = (
            self.commons["supabase"]
            .from_("brains_users")
            .select("id:brain_id, brains (id: brain_id, name)")
            .filter("user_id", "eq", user_id)
            .execute()
        )
        return [item["brains"] for item in response.data]

    def get_brain(self):
        response = (
            self.commons["supabase"]
            .from_("brains")
            .select("brainId:brain_id, brainName:brain_name")
            .filter("brain_id", "eq", self.brain_id)
            .execute()
        )
        return response.data

    def get_brain_details(self):
        response = (
            self.commons["supabase"]
            .from_("brains")
            .select("id:brain_id, name, *")
            .filter("brain_id", "eq", self.brain_id)
            .execute()
        )
        return response.data

    def delete_brain(self):
        self.commons["supabase"].table("brains").delete().match(
            {"brain_id": self.brain_id}
        ).execute()

    @classmethod
    def create_brain(cls, name):
        commons = common_dependencies()
        response = commons["supabase"].table("brains").insert({"name": name}).execute()
        # set the brainId with response.data
        return response.data

    def create_brain_user(self, brain_id, user_id, rights):
        response = (
            self.commons["supabase"]
            .table("brains_users")
            .insert({"brain_id": brain_id, "user_id": user_id, "rights": rights})
            .execute()
        )
        return response.data

    def create_brain_vector(self, vector_id):
        response = (
            self.commons["supabase"]
            .table("brains_users")
            .insert({"brain_id": self.brain_id, "vector_id": vector_id})
            .execute()
        )
        return response.data

    def get_vector_ids_from_file_sha1(self, file_sha1: str):
        # move to vectors class
        vectorsResponse = (
            self.commons["supabase"]
            .table("vectors")
            .select("id")
            .filter("metadata->>file_sha1", "eq", file_sha1)
            .execute()
        )
        return vectorsResponse.data

    def update_brain_fields(self):
        self.commons["supabase"].table("brains").update({"name": self.name}).match(
            {"brain_id": self.brain_id}
        ).execute()

    def update_brain_with_file(self, file_sha1: str):
        # not  used
        vector_ids = self.get_vector_ids_from_file_sha1(file_sha1)
        for vector_id in vector_ids:
            self.create_brain_vector(vector_id)

    def get_unique_brain_files(self):
        """
        Retrieve unique brain data (i.e. uploaded files and crawled websites).
        """

        response = (
                self.commons["supabase"]
                .from_("brains_vectors")
                .select("vector_id")
                .filter("brain_id", "eq", self.brain_id)
                .execute()
            )
        
        vector_ids = [item["vector_id"] for item in response.data]

        print('vector_ids', vector_ids)

        unique_files = self.get_unique_files_from_vector_ids(vector_ids)
        print('unique_files', unique_files)

        return unique_files

    def get_unique_files_from_vector_ids(self, vectors_ids):
        # Move into Vectors class
        """
        Retrieve unique user data vectors.
        """
        vectors_response = self.commons['supabase'].table("vectors").select(
            "name:metadata->>file_name, size:metadata->>file_size", count="exact") \
                .filter("vector_id", "in",vectors_ids)\
                .execute()
        documents = vectors_response.data  # Access the data from the response
        # Convert each dictionary to a tuple of items, then to a set to remove duplicates, and then back to a dictionary
        unique_files = [dict(t) for t in set(tuple(d.items()) for d in documents)]
        return unique_files

