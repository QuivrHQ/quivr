from uuid import UUID

from fastapi import HTTPException
from logger import get_logger
from modules.brain.entity.brain_entity import BrainType, BrainUser, RoleEnum
from modules.brain.repository.brains import Brain
from modules.brain.repository.interfaces.brains_users_interface import (
    BrainsUsersInterface,
)
from modules.brain.service.brain_service import BrainService
from modules.user.entity.user_identity import UserIdentity
from repository.api_brain_definition.get_api_brain_definition import (
    get_api_brain_definition,
)
from repository.external_api_secret.delete_secret import delete_secret

logger = get_logger(__name__)

brain_service = BrainService()


class BrainUserService:
    brain_user_repository: BrainsUsersInterface

    def __init__(self):
        self.brain_repository = Brain()

    def get_user_default_brain(self, user_id: UUID) -> BrainEntity | None:
        brain_id = self.brain_user_repository.get_user_default_brain_id(user_id)

        logger.info(f"Default brain response: {brain_id}")

        if brain_id is None:
            return None

        logger.info(f"Default brain id: {brain_id}")

        return brain_service.get_brain_by_id(brain_id)

    def delete_brain_user(self, user_id: UUID, brain_id: UUID) -> None:
        brain_to_delete_user_from = brain_service.get_brain_by_id(brain_id=brain_id)
        if brain_to_delete_user_from is None:
            raise HTTPException(status_code=404, detail="Brain not found.")

        if brain_to_delete_user_from.brain_type == BrainType.API:
            brain_definition = get_api_brain_definition(brain_id=brain_id)
            if brain_definition is None:
                raise HTTPException(
                    status_code=404, detail="Brain definition not found."
                )
            secrets = brain_definition.secrets
            for secret in secrets:
                delete_secret(
                    user_id=user_id,
                    brain_id=brain_id,
                    secret_name=secret.name,
                )

        self.brain_user_repository.delete_brain_user_by_id(
            user_id=user_id,
            brain_id=brain_id,
        )

    def get_default_user_brain_or_create_new(self, user: UserIdentity):
        default_brain = self.get_user_default_brain(user.id)

        if not default_brain:
            default_brain = brain_service.create_brain(brain=None, user_id=user.id)
            self.brain_user_repository.create_brain_user(
                user.id, default_brain.brain_id, RoleEnum.Owner, True
            )

        return default_brain

    def update_brain_user_default_status(self, brain_user: BrainUser):
        supabase_client.table("brains_users").update({"default_brain": False}).match(
            {"brain_id": brain_user.id, "user_id": brain_user.user_id}
        ).execute()

    def set_as_default_brain_for_user(self, user_id: UUID, brain_id: UUID):
        old_default_brain = self.get_user_default_brain(user_id)

        if old_default_brain is not None:
            # Add update to BrainsUsers repository -> remove default brain as default
            supabase_client.table("brains_users").update(
                {"default_brain": False}
            ).match(
                {"brain_id": old_default_brain.brain_id, "user_id": user_id}
            ).execute()
        update_brain_user_default_status
        supabase_client.table("brains_users").update({"default_brain": True}).match(
            {"brain_id": brain_id, "user_id": user_id}
        ).execute()
