import os
from typing import Any, List, Optional
from uuid import UUID

from pydantic import BaseModel
from utils.vectors import get_unique_files_from_vector_ids

from models.settings import CommonsDep, common_dependencies
from models.users import User


class Brain(BaseModel):
    id: Optional[UUID] = None
    name: Optional[str] = "Default brain"
    status: Optional[str] = "public"
    model: Optional[str] = "gpt-3.5-turbo-0613"
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = 256
    brain_size: Optional[float] = 0.0  # pyright: ignore reportPrivateUsage=none
    max_brain_size: Optional[int] = int(os.getenv("MAX_BRAIN_SIZE", 0))
    files: List[Any] = []
    _commons: Optional[CommonsDep] = None

    class Config:
        arbitrary_types_allowed = True

    @property
    def commons(self) -> CommonsDep:
        if not self._commons:
            self.__class__._commons = common_dependencies()
        return self._commons  # pyright: ignore reportPrivateUsage=none

    @property
    def brain_size(self):
        self.get_unique_brain_files()
        current_brain_size = sum(float(doc["size"]) for doc in self.files)

        print("current_brain_size", current_brain_size)
        return current_brain_size

    @property
    def remaining_brain_size(self):
        return (
            float(self.max_brain_size)  # pyright: ignore reportPrivateUsage=none
            - self.brain_size  # pyright: ignore reportPrivateUsage=none
        )

    @classmethod
    def create(cls, *args, **kwargs):
        commons = common_dependencies()
        return cls(
            commons=commons, *args, **kwargs  # pyright: ignore reportPrivateUsage=none
        )  # pyright: ignore reportPrivateUsage=none

    def get_user_brains(self, user_id):
        response = (
            self.commons["supabase"]
            .from_("brains_users")
            .select("id:brain_id, brains (id: brain_id, name)")
            .filter("user_id", "eq", user_id)
            .execute()
        )
        return [item["brains"] for item in response.data]

    def get_brain_for_user(self, user_id):
        response = (
            self.commons["supabase"]
            .from_("brains_users")
            .select("id:brain_id, rights, brains (id: brain_id, name)")
            .filter("user_id", "eq", user_id)
            .filter("brain_id", "eq", self.id)
            .execute()
        )
        if len(response.data) == 0:
            return None
        return response.data[0]

    def get_brain_details(self):
        response = (
            self.commons["supabase"]
            .from_("brains")
            .select("id:brain_id, name, *")
            .filter("brain_id", "eq", self.id)
            .execute()
        )
        return response.data

    def delete_brain(self, user_id):
        print("user_id", user_id)
        print("self.id", self.id)
        results = (
            self.commons["supabase"]
            .table("brains_users")
            .select("*")
            .match({"brain_id": self.id, "user_id": user_id, "rights": "Owner"})
            .execute()
        )
        if len(results.data) == 0:
            print("You are not the owner of this brain.")
            return {"message": "You are not the owner of this brain."}
        else:
            results = (
                self.commons["supabase"]
                .table("brains_vectors")
                .delete()
                .match({"brain_id": self.id})
                .execute()
            )
            print("results", results)

            results = (
                self.commons["supabase"]
                .table("brains_users")
                .delete()
                .match({"brain_id": self.id})
                .execute()
            )
            print("results", results)

            results = (
                self.commons["supabase"]
                .table("brains")
                .delete()
                .match({"brain_id": self.id})
                .execute()
            )
            print("results", results)

    def create_brain(self):
        commons = common_dependencies()
        response = (
            commons["supabase"].table("brains").insert({"name": self.name}).execute()
        )
        # set the brainId with response.data

        self.id = response.data[0]["brain_id"]
        return response.data

    def create_brain_user(self, user_id: UUID, rights, default_brain):
        commons = common_dependencies()
        response = (
            commons["supabase"]
            .table("brains_users")
            .insert(
                {
                    "brain_id": str(self.id),
                    "user_id": str(user_id),
                    "rights": rights,
                    "default_brain": default_brain,
                }
            )
            .execute()
        )

        return response.data

    def create_brain_vector(self, vector_id, file_sha1):
        response = (
            self.commons["supabase"]
            .table("brains_vectors")
            .insert(
                {
                    "brain_id": str(self.id),
                    "vector_id": str(vector_id),
                    "file_sha1": file_sha1,
                }
            )
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
            {"brain_id": self.id}
        ).execute()

    def update_brain_with_file(self, file_sha1: str):
        # not  used
        vector_ids = self.get_vector_ids_from_file_sha1(file_sha1)
        for vector_id in vector_ids:
            self.create_brain_vector(vector_id, file_sha1)

    def get_unique_brain_files(self):
        """
        Retrieve unique brain data (i.e. uploaded files and crawled websites).
        """

        response = (
            self.commons["supabase"]
            .from_("brains_vectors")
            .select("vector_id")
            .filter("brain_id", "eq", self.id)
            .execute()
        )

        vector_ids = [item["vector_id"] for item in response.data]

        print("vector_ids", vector_ids)

        if len(vector_ids) == 0:
            return []

        self.files = get_unique_files_from_vector_ids(vector_ids)
        print("unique_files", self.files)

        return self.files

    def delete_file_from_brain(self, file_name: str):
        # First, get the vector_ids associated with the file_name
        vector_response = (
            self.commons["supabase"]
            .table("vectors")
            .select("id")
            .filter("metadata->>file_name", "eq", file_name)
            .execute()
        )
        vector_ids = [item["id"] for item in vector_response.data]

        # For each vector_id, delete the corresponding entry from the 'brains_vectors' table
        for vector_id in vector_ids:
            self.commons["supabase"].table("brains_vectors").delete().filter(
                "vector_id", "eq", vector_id
            ).filter("brain_id", "eq", self.id).execute()

            # Check if the vector is still associated with any other brains
            associated_brains_response = (
                self.commons["supabase"]
                .table("brains_vectors")
                .select("brain_id")
                .filter("vector_id", "eq", vector_id)
                .execute()
            )
            associated_brains = [
                item["brain_id"] for item in associated_brains_response.data
            ]

            # If the vector is not associated with any other brains, delete it from 'vectors' table
            if not associated_brains:
                self.commons["supabase"].table("vectors").delete().filter(
                    "id", "eq", vector_id
                ).execute()

        return {"message": f"File {file_name} in brain {self.id} has been deleted."}


def get_default_user_brain(user: User):
    commons = common_dependencies()
    response = (
        commons["supabase"]
        .from_("brains_users")  # I'm assuming this is the correct table
        .select("brain_id")
        .filter("user_id", "eq", user.id)
        .filter(
            "default_brain", "eq", True
        )  # Assuming 'default' is the correct column name
        .execute()
    )

    print("Default brain response:", response.data)
    default_brain_id = response.data[0]["brain_id"] if response.data else None

    print(f"Default brain id: {default_brain_id}")

    if default_brain_id:
        brain_response = (
            commons["supabase"]
            .from_("brains")
            .select("id:brain_id, name, *")
            .filter("brain_id", "eq", default_brain_id)
            .execute()
        )

        return brain_response.data[0] if brain_response.data else None

    return None
