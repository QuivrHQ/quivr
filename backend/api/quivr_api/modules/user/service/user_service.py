from uuid import UUID

from quivr_api.modules.user.repository.users import Users
from quivr_api.modules.user.repository.users_interface import UsersInterface


class UserService:
    repository: UsersInterface

    def __init__(self):
        self.repository = Users()

    def get_user_id_by_email(self, email: str) -> UUID | None:
        return self.repository.get_user_id_by_user_email(email)

    def get_user_email_by_user_id(self, user_id: UUID) -> str | None:
        return self.repository.get_user_email_by_user_id(user_id)
