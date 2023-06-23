from typing import Optional
from uuid import UUID

from models.settings import CommonsDep, common_dependencies
from pydantic import BaseModel


class Brain(BaseModel):
    brain_id: Optional[UUID]
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
        vector_ids = self.get_vector_ids_from_file_sha1(file_sha1)
        for vector_id in vector_ids:
            self.create_brain_vector(vector_id)
