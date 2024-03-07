from uuid import UUID

from logger import get_logger
from models.settings import get_embeddings, get_supabase_client
from modules.brain.entity.brain_entity import BrainUser, MinimalUserBrainEntity
from modules.brain.repository.interfaces.brains_users_interface import (
    BrainsUsersInterface,
)

logger = get_logger(__name__)


class BrainsUsers(BrainsUsersInterface):
    def __init__(self):
        supabase_client = get_supabase_client()
        self.db = supabase_client

    def update_meaning(self, brain: MinimalUserBrainEntity):
        embeddings = get_embeddings()
        string_to_embed = f"Name: {brain.name} Description: {brain.description}"
        brain_meaning = embeddings.embed_query(string_to_embed)
        brain_dict = {"meaning": brain_meaning}
        response = (
            self.db.table("brains")
            .update(brain_dict)
            .match({"brain_id": brain.id})
            .execute()
        ).data

        if len(response) == 0:
            return False

        return True

    def get_user_brains(self, user_id) -> list[MinimalUserBrainEntity]:
        response = (
            self.db.from_("brains_users")
            .select(
                "id:brain_id, rights, brains (brain_id, name, status, brain_type, description, meaning, integrations_user (brain_id, integration_id, integrations (id, integration_name, integration_logo_url, max_files)))"
            )
            .filter("user_id", "eq", user_id)
            .execute()
        )
        user_brains: list[MinimalUserBrainEntity] = []
        for item in response.data:
            integration_logo_url = ""
            max_files = 5000
            if item["brains"]["brain_type"] == "integration":
                if "integrations_user" in item["brains"]:
                    for integration_user in item["brains"]["integrations_user"]:
                        if "integrations" in integration_user:
                            integration_logo_url = integration_user["integrations"][
                                "integration_logo_url"
                            ]
                            max_files = integration_user["integrations"]["max_files"]

            user_brains.append(
                MinimalUserBrainEntity(
                    id=item["brains"]["brain_id"],
                    name=item["brains"]["name"],
                    rights=item["rights"],
                    status=item["brains"]["status"],
                    brain_type=item["brains"]["brain_type"],
                    description=(
                        item["brains"]["description"]
                        if item["brains"]["description"] is not None
                        else ""
                    ),
                    integration_logo_url=str(integration_logo_url),
                    max_files=max_files,
                )
            )
            user_brains[-1].rights = item["rights"]
            if item["brains"]["meaning"] is None:
                self.update_meaning(user_brains[-1])

        return user_brains

    def get_brain_for_user(self, user_id, brain_id):
        response = (
            self.db.from_("brains_users")
            .select(
                "id:brain_id, rights, brains (id: brain_id, status, name, brain_type, description)"
            )
            .filter("user_id", "eq", user_id)
            .filter("brain_id", "eq", brain_id)
            .execute()
        )
        if len(response.data) == 0:
            return None
        brain_data = response.data[0]

        return MinimalUserBrainEntity(
            id=brain_data["brains"]["id"],
            name=brain_data["brains"]["name"],
            rights=brain_data["rights"],
            status=brain_data["brains"]["status"],
            brain_type=brain_data["brains"]["brain_type"],
            description=(
                brain_data["brains"]["description"]
                if brain_data["brains"]["description"] is not None
                else ""
            ),
            integration_logo_url="",
            max_files=100,
        )

    def delete_brain_user_by_id(
        self,
        user_id: UUID,
        brain_id: UUID,
    ):
        results = (
            self.db.table("brains_users")
            .delete()
            .match({"brain_id": str(brain_id), "user_id": str(user_id)})
            .execute()
        )
        return results.data

    def delete_brain_users(self, brain_id: str):
        results = (
            self.db.table("brains_users")
            .delete()
            .match({"brain_id": brain_id})
            .execute()
        )

        return results

    def create_brain_user(self, user_id: UUID, brain_id, rights, default_brain: bool):
        response = (
            self.db.table("brains_users")
            .insert(
                {
                    "brain_id": str(brain_id),
                    "user_id": str(user_id),
                    "rights": rights,
                    "default_brain": default_brain,
                }
            )
            .execute()
        )
        return response

    def get_user_default_brain_id(self, user_id: UUID) -> UUID | None:
        response = (
            (
                self.db.from_("brains_users")
                .select("brain_id")
                .filter("user_id", "eq", user_id)
                .filter("default_brain", "eq", True)
                .execute()
            )
        ).data
        if len(response) == 0:
            return None
        return UUID(response[0].get("brain_id"))

    def get_brain_users(self, brain_id: UUID) -> list[BrainUser]:
        response = (
            self.db.table("brains_users")
            .select("id:brain_id, *")
            .filter("brain_id", "eq", str(brain_id))
            .execute()
        )

        return [BrainUser(**item) for item in response.data]

    def delete_brain_subscribers(self, brain_id: UUID):
        results = (
            self.db.table("brains_users")
            .delete()
            .match({"brain_id": str(brain_id)})
            .match({"rights": "Viewer"})
            .execute()
        ).data

        return results

    def get_brain_subscribers_count(self, brain_id: UUID) -> int:
        response = (
            self.db.from_("brains_users")
            .select(
                "count",
            )
            .filter("brain_id", "eq", str(brain_id))
            .execute()
        ).data
        if len(response) == 0:
            raise ValueError(f"Brain with id {brain_id} does not exist.")
        return response[0]["count"]

    def update_brain_user_default_status(
        self, user_id: UUID, brain_id: UUID, default_brain: bool
    ):
        self.db.table("brains_users").update({"default_brain": default_brain}).match(
            {"brain_id": brain_id, "user_id": user_id}
        ).execute()

    def update_brain_user_rights(
        self, user_id: UUID, brain_id: UUID, rights: str
    ) -> None:
        self.db.table("brains_users").update({"rights": rights}).match(
            {"brain_id": brain_id, "user_id": user_id}
        ).execute()
