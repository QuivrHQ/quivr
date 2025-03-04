from uuid import UUID

from quivr_api.modules.user.dto.inputs import CreateUserRequest, UserUpdatableProperties
from quivr_api.modules.user.repository.users import Users
from quivr_api.modules.user.repository.users_interface import UsersInterface
from quivr_api.modules.dependencies import get_supabase_client


class UserService:
    repository: UsersInterface

    def __init__(self):
        self.repository = Users()
        self.supabase_client = get_supabase_client()

    def get_user_id_by_email(self, email: str) -> UUID | None:
        return self.repository.get_user_id_by_user_email(email)

    def get_user_email_by_user_id(self, user_id: UUID) -> str | None:
        return self.repository.get_user_email_by_user_id(user_id)
        
    def create_user(self, user_data: CreateUserRequest):
        """Create a new user with Supabase Auth and associate with brains"""
        # Create user in Supabase Auth
        auth_response = self.supabase_client.auth.admin.create_user({
            "email": user_data.email,
            "password": "admin123",
            "email_confirm": False,
            "user_metadata": {
                "first_name": user_data.firstName,
                "last_name": user_data.lastName,
            }
        })
        
        if not auth_response.user:
            raise Exception("Failed to create user in Supabase Auth")
            
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
                
            self.supabase.table("brains_users").insert(brain_user_entries).execute()
            
        return {
            "id": user_id,
            "email": user_data.email,
            "username": f"{user_data.firstName} {user_data.lastName}"
        }
