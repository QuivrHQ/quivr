from uuid import UUID

from quivr_core.api.modules.dependencies import BaseService
from quivr_core.api.modules.user.dto.inputs import UserUpdatableProperties
from quivr_core.api.modules.user.repository.user_repository import UserRepository


class UserService(BaseService[UserRepository]):
    repository_cls = UserRepository

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user_id_by_email(self, email: str) -> UUID | None:
        return self.repository.get_user_id_by_user_email(email)

    def get_user_email_by_user_id(self, user_id: UUID) -> str | None:
        return self.repository.get_user_email_by_user_id(user_id)

    def get_user_settings(self, user_id: UUID):
        return self.repository.get_user_settings(user_id)

    def get_user_identity(self, user_id: UUID):
        return self.repository.get_user_identity(user_id)

    def update_user_properties(
        self,
        user_id: UUID,
        user_identity_updatable_properties: UserUpdatableProperties,
    ):
        return self.repository.update_user_properties(
            user_id, user_identity_updatable_properties
        )

    def delete_user_data(self, user_id: UUID):
        return self.repository.delete_user_data(user_id)
