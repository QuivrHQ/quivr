import os
from typing import Any, List, Optional
from uuid import UUID
from utils.vectors import get_unique_files_from_vector_ids

from logger import get_logger
from models.settings import CommonsDep, common_dependencies
from models.users import User
from pydantic import BaseModel

logger = get_logger(__name__)


class Brain(BaseModel):
    id: Optional[UUID] = None
    name: Optional[str] = "Default brain"
    status: Optional[str] = "public"
    model: Optional[str] = "gpt-3.5-turbo-0613"
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = 256
    max_brain_size: Optional[int] = int(os.getenv("MAX_BRAIN_SIZE", 52428800))
    files: List[Any] = []

    class Config:
        arbitrary_types_allowed = True

    @property
    def commons(self) -> CommonsDep:
        return common_dependencies()

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
        commons = common_dependencies()
        return cls(
            commons=commons, *args, **kwargs  # pyright: ignore reportPrivateUsage=none
        )  # pyright: ignore reportPrivateUsage=none

    def get_user_brains(self, user_id):
        return self.commons["db"].get_user_brains(user_id)

    def get_brain_for_user(self, user_id):
        return self.commons["db"].get_brain_for_user(user_id, self.id)

    def get_brain_details(self):
        return self.commons["db"].get_brain_details(self.id)

    def delete_brain(self, user_id):
        return self.commons["db"].delete_brain(user_id, self.id)

    def create_brain(self):
        response = self.commons["db"].create_brain(self.name)
        self.id = response.data[0]["brain_id"]
        return response.data

    def create_brain_user(self, user_id: UUID, rights, default_brain):
        return self.commons["db"].create_brain_user(user_id=user_id, brain_id=self.id, rights=rights, default_brain=default_brain)


    def create_brain_vector(self, vector_id, file_sha1):
        return self.commons["db"].create_brain_vector(self.id, vector_id, file_sha1)

    def get_vector_ids_from_file_sha1(self, file_sha1: str):
        return self.commons["db"].get_vector_ids_from_file_sha1(file_sha1)

    def update_brain_fields(self):
        return self.commons["db"].update_brain_fields(brain_id=self.id, brain_name=self.name)

    def update_brain_with_file(self, file_sha1: str):
        # not  used
        vector_ids = self.get_vector_ids_from_file_sha1(file_sha1)
        for vector_id in vector_ids:
            self.create_brain_vector(vector_id, file_sha1)

    def get_unique_brain_files(self):
        """
        Retrieve unique brain data (i.e. uploaded files and crawled websites).
        """

        vector_ids = self.commons["db"].get_brain_vector_ids(self.id)
        self.files = get_unique_files_from_vector_ids(vector_ids)

        return self.files

    def delete_file_from_brain(self, file_name: str):
        return self.commons["db"].delete_file_from_brain(self.id, file_name)


def get_default_user_brain(user: User):
    commons = common_dependencies()
    response = commons["db"].get_default_user_brain_id(user.id)
       
    logger.info("Default brain response:", response.data)
    default_brain_id = response.data[0]["brain_id"] if response.data else None

    logger.info(f"Default brain id: {default_brain_id}")

    if default_brain_id:
        brain_response = commons["db"].get_brain_by_id(default_brain_id)
        return brain_response.data[0] if brain_response.data else None
