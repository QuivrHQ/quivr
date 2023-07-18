from abc import ABC, abstractmethod
from uuid import UUID


class Database(ABC):
    @abstractmethod
    def get_user_brains(self, user_id):
        pass

    @abstractmethod
    def get_brain_for_user(self, user_id):
        pass

    @abstractmethod
    def delete_brain(self, user_id, brain_id):
        pass

    @abstractmethod
    def create_brain(self, name):
        pass

    @abstractmethod
    def create_brain_user(self, user_id: UUID, brain_id, rights, default_brain):
        pass

    @abstractmethod
    def create_brain_vector(self, brain_id, vector_id, file_sha1):
        pass

    @abstractmethod
    def get_vector_ids_from_file_sha1(self, file_sha1: str):
        pass

    @abstractmethod
    def update_brain_fields(self, brain_id, brain_name):
        pass

    @abstractmethod
    def get_brain_vector_ids(self, brain_id):
        pass

    @abstractmethod
    def delete_file_from_brain(self, brain_id, file_name: str):
        pass

    @abstractmethod
    def get_default_user_brain(self, user_id: UUID):
        pass