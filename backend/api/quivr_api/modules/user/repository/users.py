import time
from typing import List

from quivr_api.modules.dependencies import get_supabase_client
from quivr_api.modules.user.entity.user_identity import UserIdentity
from quivr_api.modules.user.repository.users_interface import UsersInterface
from quivr_api.modules.user.service import user_usage


class Users(UsersInterface):
    def __init__(self):
        supabase_client = get_supabase_client()
        self.db = supabase_client

    def create_user_identity(self, id):
        response = (
            self.db.from_("user_identity")
            .insert(
                {
                    "user_id": str(id),
                }
            )
            .execute()
        )
        user_identity = response.data[0]
        return UserIdentity(id=user_identity.get("user_id"))

    def update_user_properties(
        self,
        user_id,
        user_identity_updatable_properties,
    ):
        response = (
            self.db.from_("user_identity")
            .update(user_identity_updatable_properties.__dict__)
            .filter("user_id", "eq", user_id)  # type: ignore
            .execute()
        )

        if len(response.data) == 0:
            return self.create_user_identity(user_id)

        user_identity = response.data[0]

        return UserIdentity(id=user_id)

    def get_user_identity(self, user_id):
        response = (
            self.db.from_("user_identity")
            .select("*, users (email)")
            .filter("user_id", "eq", str(user_id))
            .execute()
        )

        if len(response.data) == 0:
            return self.create_user_identity(user_id)

        user_identity = response.data[0]

        user_identity["id"] = user_id  # Add 'id' field to the dictionary
        user_identity["email"] = user_identity["users"]["email"]
        
        # Get user's brains
        brains_response = (
            self.db.from_("brains_users")
            .select("brain_id")
            .filter("user_id", "eq", str(user_id))
            .execute()
        )
        
        user_identity["brains"] = [brain["brain_id"] for brain in brains_response.data]
        
        return UserIdentity(**user_identity)
        
    def get_all_users(self) -> List[UserIdentity]:
        """
        Get all users in the system
        
        Returns a list of all user identities with their associated brains and last login time
        """
        try:
            # First, get all user identities from the public schema
            user_identity_response = (
                self.db.from_("user_identity")
                .select("*")
                .execute()
            )
            print(f"user_identity_response: {user_identity_response}")
            
            # Get all users from the auth schema using the auth admin API
            auth_users_response = self.db.auth.admin.list_users()
            print(f"auth_users_response type: {type(auth_users_response)}")
            print(f"auth_users_response: {auth_users_response}")

            # Create a mapping of user IDs to auth user data for easy lookup
            # Handle different possible response structures
            auth_users_map = {}
            if hasattr(auth_users_response, "users"):
                auth_users_map = {user["id"]: user for user in auth_users_response.users}
            elif isinstance(auth_users_response, list):
                auth_users_map = {user.id: user for user in auth_users_response}
            elif hasattr(auth_users_response, "data") and isinstance(auth_users_response.data, list):
                auth_users_map = {user["id"]: user for user in auth_users_response.data}
            
            print(f"auth_users_map: {auth_users_map}")
            
            # Fetch all brains to create a mapping of brain IDs to brain names
            brains_response = (
                self.db.from_("brains")
                .select("brain_id, name")
                .execute()
            )
            
            # Create a mapping of brain IDs to brain names for easy lookup
            brain_id_to_name = {str(brain["brain_id"]): brain["name"] for brain in brains_response.data}
            print(f"brain_id_to_name: {brain_id_to_name}")
            
            users = []
            for user_data in user_identity_response.data:
                user_id = user_data.get("user_id")
                if user_id:
                    # Map user_id to id for the UserIdentity model
                    user_data["id"] = user_id
                    
                    # Get auth user data if available
                    auth_user = auth_users_map.get(user_id)
                    if auth_user:
                        # Handle different object structures (dict vs object)
                        if isinstance(auth_user, dict):
                            user_data["email"] = auth_user.get("email")
                            last_sign_in = auth_user.get("last_sign_in_at")
                            # Convert datetime to string if needed
                            if last_sign_in and not isinstance(last_sign_in, str):
                                user_data["last_sign_in_at"] = last_sign_in.isoformat() if hasattr(last_sign_in, "isoformat") else str(last_sign_in)
                            else:
                                user_data["last_sign_in_at"] = last_sign_in
                        else:
                            # Handle object-like structure
                            user_data["email"] = getattr(auth_user, "email", None)
                            last_sign_in = getattr(auth_user, "last_sign_in_at", None)
                            # Convert datetime to string if needed
                            if last_sign_in and not isinstance(last_sign_in, str):
                                user_data["last_sign_in_at"] = last_sign_in.isoformat() if hasattr(last_sign_in, "isoformat") else str(last_sign_in)
                            else:
                                user_data["last_sign_in_at"] = last_sign_in
                    else:
                        # Try to get email from get_user_email_by_user_id method
                        try:
                            user_data["email"] = self.get_user_email_by_user_id(user_id)
                        except Exception as e:
                            user_data["email"] = None
                    
                    # Get user's brains
                    brains_users_response = (
                        self.db.from_("brains_users")
                        .select("brain_id")
                        .filter("user_id", "eq", str(user_id))
                        .execute()
                    )
                    
                    print(f"brains_users_response for user {user_id}: {brains_users_response}")
                    
                    # Map brain IDs to brain names
                    brain_ids = [brain["brain_id"] for brain in brains_users_response.data]
                    brain_names = [brain_id_to_name.get(str(brain_id), f"Unknown Brain ({brain_id})") for brain_id in brain_ids]
                    
                    # Store both brain IDs and brain names
                    user_data["brains"] = brain_ids
                    user_data["brain_names"] = brain_names
                    
                    # Debug the user_data before creating UserIdentity
                    print(f"User data for {user_id}: {user_data}")
                    
                    try:
                        # Convert user_id to UUID if it's a string
                        if isinstance(user_data["id"], str):
                            from uuid import UUID
                            user_data["id"] = UUID(user_data["id"])
                            
                        user_identity = UserIdentity(**user_data)
                        users.append(user_identity)
                    except Exception as e:
                        print(f"Error creating UserIdentity for user {user_id}: {str(e)}")
            
            return users
        except Exception as e:
            # Log the error and re-raise with more context
            print(f"Error in get_all_users: {str(e)}")
            raise Exception(f"Failed to retrieve users: {str(e)}")

    def get_user_id_by_user_email(self, email):
        response = (
            self.db.rpc("get_user_id_by_user_email", {"user_email": email})
            .execute()
            .data
        )
        if len(response) > 0:
            return response[0]["user_id"]
        return None

    def get_user_email_by_user_id(self, user_id):
        response = self.db.rpc(
            "get_user_email_by_user_id", {"user_id": str(user_id)}
        ).execute()
        return response.data[0]["email"]

    def delete_user_data(self, user_id):
        response = (
            self.db.from_("brains_users")
            .select("brain_id")
            .filter("rights", "eq", "Owner")
            .filter("user_id", "eq", str(user_id))
            .execute()
        )
        brain_ids = [row["brain_id"] for row in response.data]

        for brain_id in brain_ids:
            self.db.table("brains").delete().filter(
                "brain_id", "eq", brain_id
            ).execute()

        for brain_id in brain_ids:
            self.db.table("brains_vectors").delete().filter(
                "brain_id", "eq", brain_id
            ).execute()

        for brain_id in brain_ids:
            self.db.table("chat_history").delete().filter(
                "brain_id", "eq", brain_id
            ).execute()

        self.db.table("user_settings").delete().filter(
            "user_id", "eq", str(user_id)
        ).execute()
        self.db.table("user_identity").delete().filter(
            "user_id", "eq", str(user_id)
        ).execute()
        self.db.table("users").delete().filter("id", "eq", str(user_id)).execute()

    def get_user_credits(self, user_id):
        try:
            user_usage_instance = user_usage.UserUsage(id=user_id)

            user_monthly_usage = user_usage_instance.get_user_monthly_usage(
                time.strftime("%Y%m%d")
            )
            
            response = self.db.from_("user_settings").select("monthly_chat_credit").filter(
                "user_id", "eq", str(user_id)
            ).execute()
            
            if not response.data:
                raise ValueError("No data found for user settings")

            monthly_chat_credit = response.data[0].get("monthly_chat_credit")
            if monthly_chat_credit is None:
                raise ValueError("Monthly chat credit not found")

            return monthly_chat_credit - user_monthly_usage

        except Exception as e:
            # Log the exception or handle it as needed
            print(f"An error occurred while getting user credits: {e}")
            return 25  # or a default value, depending on your needs
