from uuid import UUID

from quivr_api.modules.dependencies import BaseService
from quivr_core.api.modules.user.repository.users import UserRepository


class UserService(BaseService[UserRepository]):
    repository_cls = UserRepository

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user_id_by_email(self, email: str) -> UUID | None:
        return self.repository.get_user_id_by_user_email(email)

    def get_user_email_by_user_id(self, user_id: UUID) -> str | None:
        return self.repository.get_user_email_by_user_id(user_id)
