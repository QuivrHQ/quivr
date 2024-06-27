import time

from quivr_api.models.settings import get_supabase_client
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

        print("USER_IDENTITY", user_identity)
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
        return UserIdentity(**user_identity)

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
        user_usage_instance = user_usage.UserUsage(id=user_id)

        user_monthly_usage = user_usage_instance.get_user_monthly_usage(
            time.strftime("%Y%m%d")
        )
        monthly_chat_credit = (
            self.db.from_("user_settings")
            .select("monthly_chat_credit")
            .filter("user_id", "eq", str(user_id))
            .execute()
            .data[0]["monthly_chat_credit"]
        )

        return monthly_chat_credit - user_monthly_usage
