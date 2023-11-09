from typing import Optional
from uuid import UUID

from logger import get_logger
from models.brain_entity import BrainEntity, BrainType, MinimalBrainEntity, PublicBrain
from models.databases.repository import Repository
from models.databases.supabase.api_brain_definition import (
    CreateApiBrainDefinition,
)
from pydantic import BaseModel, Extra

logger = get_logger(__name__)


class CreateBrainProperties(BaseModel, extra=Extra.forbid):
    name: Optional[str] = "Default brain"
    description: Optional[str] = "This is a description"
    status: Optional[str] = "private"
    model: Optional[str]
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = 256
    openai_api_key: Optional[str] = None
    prompt_id: Optional[UUID] = None
    brain_type: Optional[BrainType] = BrainType.DOC
    brain_definition: Optional[CreateApiBrainDefinition]
    brain_secrets_values: dict = {}

    def dict(self, *args, **kwargs):
        brain_dict = super().dict(*args, **kwargs)
        if brain_dict.get("prompt_id"):
            brain_dict["prompt_id"] = str(brain_dict.get("prompt_id"))
        return brain_dict


class BrainUpdatableProperties(BaseModel):
    name: Optional[str]
    description: Optional[str]
    temperature: Optional[float]
    model: Optional[str]
    max_tokens: Optional[int]
    openai_api_key: Optional[str]
    status: Optional[str]
    prompt_id: Optional[UUID]

    def dict(self, *args, **kwargs):
        brain_dict = super().dict(*args, **kwargs)
        if brain_dict.get("prompt_id"):
            brain_dict["prompt_id"] = str(brain_dict.get("prompt_id"))
        return brain_dict


class BrainQuestionRequest(BaseModel):
    question: str


class Brain(Repository):
    def __init__(self, supabase_client):
        self.db = supabase_client

    def create_brain(self, brain: CreateBrainProperties):
        response = (
            self.db.table("brains").insert(
                brain.dict(exclude={"brain_definition", "brain_secrets_values"})
            )
        ).execute()

        return BrainEntity(**response.data[0])

    def get_user_brains(self, user_id) -> list[MinimalBrainEntity]:
        response = (
            self.db.from_("brains_users")
            .select("id:brain_id, rights, brains (brain_id, name, status)")
            .filter("user_id", "eq", user_id)
            .execute()
        )
        user_brains: list[MinimalBrainEntity] = []
        for item in response.data:
            user_brains.append(
                MinimalBrainEntity(
                    id=item["brains"]["brain_id"],
                    name=item["brains"]["name"],
                    rights=item["rights"],
                    status=item["brains"]["status"],
                )
            )
            user_brains[-1].rights = item["rights"]
        return user_brains

    def get_public_brains(self) -> list[PublicBrain]:
        response = (
            self.db.from_("brains")
            .select("id:brain_id, name, description, last_update")
            .filter("status", "eq", "public")
            .execute()
        )
        public_brains: list[PublicBrain] = []
        for item in response.data:
            brain = PublicBrain(
                id=item["id"],
                name=item["name"],
                description=item["description"],
                last_update=item["last_update"],
            )
            brain.number_of_subscribers = self.get_brain_subscribers_count(brain.id)
            public_brains.append(brain)
        return public_brains

    def update_brain_last_update_time(self, brain_id: UUID) -> None:
        self.db.table("brains").update({"last_update": "now()"}).match(
            {"brain_id": brain_id}
        ).execute()

    def get_brain_for_user(self, user_id, brain_id) -> MinimalBrainEntity | None:
        response = (
            self.db.from_("brains_users")
            .select("id:brain_id, rights, brains (id: brain_id, status, name)")
            .filter("user_id", "eq", user_id)
            .filter("brain_id", "eq", brain_id)
            .execute()
        )
        if len(response.data) == 0:
            return None
        brain_data = response.data[0]

        return MinimalBrainEntity(
            id=brain_data["brains"]["id"],
            name=brain_data["brains"]["name"],
            rights=brain_data["rights"],
            status=brain_data["brains"]["status"],
        )

    def get_brain_details(self, brain_id):
        response = (
            self.db.from_("brains")
            .select("id:brain_id, name, *")
            .filter("brain_id", "eq", brain_id)
            .execute()
        )
        return response.data

    def delete_brain_user_by_id(
        self,
        user_id: UUID,
        brain_id: UUID,
    ):
        results = (
            self.db.table("brains_users")
            .delete()
            .match({"brain_id": str(brain_id), "user_id": str(user_id)})
            .execute()
        )
        return results.data

    def delete_brain_vector(self, brain_id: str):
        results = (
            self.db.table("brains_vectors")
            .delete()
            .match({"brain_id": brain_id})
            .execute()
        )

        return results

    def delete_brain_users(self, brain_id: str):
        results = (
            self.db.table("brains_users")
            .delete()
            .match({"brain_id": brain_id})
            .execute()
        )

        return results

    def delete_brain_subscribers(self, brain_id: UUID):
        results = (
            self.db.table("brains_users")
            .delete()
            .match({"brain_id": str(brain_id)})
            .match({"rights": "Viewer"})
            .execute()
        ).data

        return results

    def delete_brain(self, brain_id: str):
        results = (
            self.db.table("brains").delete().match({"brain_id": brain_id}).execute()
        )

        return results

    def create_brain_user(self, user_id: UUID, brain_id, rights, default_brain: bool):
        response = (
            self.db.table("brains_users")
            .insert(
                {
                    "brain_id": str(brain_id),
                    "user_id": str(user_id),
                    "rights": rights,
                    "default_brain": default_brain,
                }
            )
            .execute()
        )

        return response

    def create_brain_vector(self, brain_id, vector_id, file_sha1):
        response = (
            self.db.table("brains_vectors")
            .insert(
                {
                    "brain_id": str(brain_id),
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
            self.db.table("vectors")
            .select("id")
            .filter("file_sha1", "eq", file_sha1)
            .execute()
        )
        return vectorsResponse.data

    def update_brain_by_id(
        self, brain_id: UUID, brain: BrainUpdatableProperties
    ) -> BrainEntity | None:
        update_brain_response = (
            self.db.table("brains")
            .update(brain.dict(exclude_unset=True))
            .match({"brain_id": brain_id})
            .execute()
        ).data

        if len(update_brain_response) == 0:
            return None

        return BrainEntity(**update_brain_response[0])

    def get_brain_vector_ids(self, brain_id):
        """
        Retrieve unique brain data (i.e. uploaded files and crawled websites).
        """

        response = (
            self.db.from_("brains_vectors")
            .select("vector_id")
            .filter("brain_id", "eq", brain_id)
            .execute()
        )

        vector_ids = [item["vector_id"] for item in response.data]

        if len(vector_ids) == 0:
            return []

        return vector_ids

    def delete_file_from_brain(self, brain_id, file_name: str):
        # First, get the vector_ids associated with the file_name
        vector_response = (
            self.db.table("vectors")
            .select("id")
            .filter("metadata->>file_name", "eq", file_name)
            .execute()
        )
        vector_ids = [item["id"] for item in vector_response.data]

        # For each vector_id, delete the corresponding entry from the 'brains_vectors' table
        for vector_id in vector_ids:
            self.db.table("brains_vectors").delete().filter(
                "vector_id", "eq", vector_id
            ).filter("brain_id", "eq", brain_id).execute()

            # Check if the vector is still associated with any other brains
            associated_brains_response = (
                self.db.table("brains_vectors")
                .select("brain_id")
                .filter("vector_id", "eq", vector_id)
                .execute()
            )
            associated_brains = [
                item["brain_id"] for item in associated_brains_response.data
            ]

            # If the vector is not associated with any other brains, delete it from 'vectors' table
            if not associated_brains:
                self.db.table("vectors").delete().filter(
                    "id", "eq", vector_id
                ).execute()

        return {"message": f"File {file_name} in brain {brain_id} has been deleted."}

    def get_default_user_brain_id(self, user_id: UUID) -> UUID | None:
        response = (
            (
                self.db.from_("brains_users")
                .select("brain_id")
                .filter("user_id", "eq", user_id)
                .filter("default_brain", "eq", True)
                .execute()
            )
        ).data
        if len(response) == 0:
            return None
        return UUID(response[0].get("brain_id"))

    def get_brain_by_id(self, brain_id: UUID) -> BrainEntity | None:
        response = (
            self.db.from_("brains")
            .select("id:brain_id, name, *")
            .filter("brain_id", "eq", brain_id)
            .execute()
        ).data

        if len(response) == 0:
            return None

        return BrainEntity(**response[0])

    def get_brain_subscribers_count(self, brain_id: UUID) -> int:
        response = (
            self.db.from_("brains_users")
            .select(
                "count",
            )
            .filter("brain_id", "eq", str(brain_id))
            .execute()
        ).data
        if len(response) == 0:
            raise ValueError(f"Brain with id {brain_id} does not exist.")
        return response[0]["count"]
