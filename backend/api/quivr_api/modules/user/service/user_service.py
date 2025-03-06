from typing import List
from uuid import UUID, uuid4

from quivr_api.modules.user.dto.inputs import CreateUserRequest, UserUpdatableProperties
from quivr_api.modules.user.entity.user_identity import UserIdentity
from quivr_api.modules.user.repository.users import Users
from quivr_api.modules.user.repository.users_interface import UsersInterface
from quivr_api.modules.dependencies import get_supabase_client
from quivr_api.logger import get_logger
from quivr_api.utils.send_email import send_email

import os

logger = get_logger(__name__)

def generate_uuid_password() -> str:
    return str(uuid4())

class UserService:
    repository: UsersInterface

    def __init__(self):
        self.repository = Users()
        self.supabase_client = get_supabase_client()

    def get_user_id_by_email(self, email: str) -> UUID | None:
        return self.repository.get_user_id_by_user_email(email)

    def get_user_email_by_user_id(self, user_id: UUID) -> str | None:
        return self.repository.get_user_email_by_user_id(user_id)

    def get_all_users(self) -> List[UserIdentity]:
        """
        Get all users in the system

        Returns a list of all user identities
        """
        return self.repository.get_all_users()

    def create_user(self, user_data: CreateUserRequest):
        """Create a new user with Supabase Auth and associate with brains"""

        # Random uuid password
        password = generate_uuid_password();

        # Create user in Supabase Auth
        auth_response = self.supabase_client.auth.admin.create_user({
            "email": user_data.email,
            "password": password,
            "email_confirm": False,
            "user_metadata": {
                "first_name": user_data.firstName,
                "last_name": user_data.lastName,
            }
        })

        if not auth_response.user:
            raise Exception("Failed to create user in Supabase Auth")

        # Send email to user
        self.resend_invitation_email(
            f"{user_data.lastName} {user_data.firstName}",
            user_data.email,
            password
        )

        user_id = auth_response.user.id

        # Create user identity
        user_identity = self.repository.create_user_identity(user_id)

        # Update username
        self.repository.update_user_properties(
            user_id,
            UserUpdatableProperties(
                username=f"{user_data.firstName} {user_data.lastName}",
                onboarded=True
            )
        )

        # Associate user with brains
        if user_data.brains:
            brain_user_entries = []
            for brain_id in user_data.brains:
                brain_user_entries.append({
                    "brain_id": brain_id,
                    "user_id": user_id,
                    "rights": "Viewer"
                })

            self.supabase_client.table("brains_users").insert(brain_user_entries).execute()

        return {
            "id": user_id,
            "email": user_data.email,
            "username": f"{user_data.firstName} {user_data.lastName}"
        }

    def resend_invitation_email(
        self,
        fullNameUser: str,
        email: str,
        password: str,
    ):
        html_body = f"""
        <p>Chào {fullNameUser},</p>

        <p>Chúng tôi mời bạn tham gia vào <b>Dự án Medzavy</b>.</p>

        <p>Thông tin đăng nhập của bạn:</p>

        <ul>
            <li><b>Email:</b> {email}</li>
            <li><b>Password:</b> {password}</li>
        </ul>

        <p>Để bắt đầu, vui lòng nhấn vào liên kết dưới đây:</p>
        <p><a href='{os.getenv("QUIVR_DOMAIN")}' style="color: blue; font-weight: bold;">Bấm vào đây để tham gia Dự án Medzavy</a></p>

        <p><b>Lưu ý:</b> Vì lý do bảo mật, hãy thay đổi mật khẩu sau khi đăng nhập lần đầu.</p>

        <p>Trân trọng,<br>Đội ngũ Medzavy</p>
        """

        try:
            r = send_email(
                {
                    "from": "no-reply@medzavy.app",
                    "to": [email],
                    "subject": "Medzavy - Thư mời tham gia dự án",
                    "reply_to": "no-reply@medzavy.app",
                    "html": html_body,
                }
            )
            logger.info("Resend response", r)
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return

        return r
