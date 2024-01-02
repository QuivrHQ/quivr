from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID


class Repository(ABC):
    @abstractmethod
    def create_user_daily_usage(self, user_id: UUID, user_email: str, date: datetime):
        pass

    @abstractmethod
    def get_user_usage(self, user_id: UUID):
        pass

    @abstractmethod
    def get_user_requests_count_for_day(self, user_id: UUID, date: datetime):
        pass

    @abstractmethod
    def update_user_request_count(self, user_id: UUID, date: str):
        pass

    @abstractmethod
    def increment_user_request_count(
        self, user_id: UUID, date: str, current_request_count
    ):
        pass

    @abstractmethod
    def set_file_vectors_ids(self, file_sha1: str):
        pass

    @abstractmethod
    def get_brain_vectors_by_brain_id_and_file_sha1(
        self, brain_id: UUID, file_sha1: str
    ):
        pass

    @abstractmethod
    def create_subscription_invitation(
        self, brain_id: UUID, user_email: str, rights: str
    ):
        pass

    @abstractmethod
    def update_subscription_invitation(
        self, brain_id: UUID, user_email: str, rights: str
    ):
        pass

    @abstractmethod
    def get_subscription_invitations_by_brain_id_and_email(
        self, brain_id: UUID, user_email: str
    ):
        pass

    @abstractmethod
    def get_vectors_by_file_name(self, file_name: str):
        pass

    @abstractmethod
    def similarity_search(
        self, query_embedding, table: str, top_k: int, threshold: float
    ):
        pass

    @abstractmethod
    def update_summary(self, document_id: UUID, summary_id: int):
        pass

    @abstractmethod
    def get_vectors_by_batch(self, batch_id: UUID):
        pass

    @abstractmethod
    def get_vectors_in_batch(self, batch_ids):
        pass

    @abstractmethod
    def get_vectors_by_file_sha1(self, file_sha1):
        pass
