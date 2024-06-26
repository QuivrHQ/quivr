from typing import List
from uuid import UUID

from fastapi import HTTPException
from quivr_api.logger import get_logger
from quivr_api.modules.brain.entity.brain_entity import (
    BrainEntity,
    BrainType,
    BrainUser,
    MinimalUserBrainEntity,
    RoleEnum,
)
from quivr_api.modules.brain.repository.brains import Brains
from quivr_api.modules.brain.repository.brains_users import BrainsUsers
from quivr_api.modules.brain.repository.external_api_secrets import ExternalApiSecrets
from quivr_api.modules.brain.repository.interfaces.brains_interface import (
    BrainsInterface,
)
from quivr_api.modules.brain.repository.interfaces.brains_users_interface import (
    BrainsUsersInterface,
)
from quivr_api.modules.brain.repository.interfaces.external_api_secrets_interface import (
    ExternalApiSecretsInterface,
)
from quivr_api.modules.brain.service.api_brain_definition_service import (
    ApiBrainDefinitionService,
)
from quivr_api.modules.brain.service.brain_service import BrainService

logger = get_logger(__name__)

brain_service = BrainService()
api_brain_definition_service = ApiBrainDefinitionService()


class BrainUserService:
    brain_repository: BrainsInterface
    brain_user_repository: BrainsUsersInterface
    external_api_secrets_repository: ExternalApiSecretsInterface

    def __init__(self):
        self.brain_repository = Brains()
        self.brain_user_repository = BrainsUsers()
        self.external_api_secrets_repository = ExternalApiSecrets()

    def get_user_default_brain(self, user_id: UUID) -> BrainEntity | None:
        brain_id = self.brain_user_repository.get_user_default_brain_id(user_id)

        if brain_id is None:
            return None

        return brain_service.get_brain_by_id(brain_id)

    def delete_brain_user(self, user_id: UUID, brain_id: UUID) -> None:
        brain_to_delete_user_from = brain_service.get_brain_by_id(brain_id=brain_id)
        if brain_to_delete_user_from is None:
            raise HTTPException(status_code=404, detail="Brain not found.")

        if brain_to_delete_user_from.brain_type == BrainType.api:
            brain_definition = api_brain_definition_service.get_api_brain_definition(
                brain_id=brain_id
            )
            if brain_definition is None:
                raise HTTPException(
                    status_code=404, detail="Brain definition not found."
                )
            secrets = brain_definition.secrets
            for secret in secrets:
                self.external_api_secrets_repository.delete_secret(
                    user_id=user_id,
                    brain_id=brain_id,
                    secret_name=secret.name,
                )

        self.brain_user_repository.delete_brain_user_by_id(
            user_id=user_id,
            brain_id=brain_id,
        )

    def delete_brain_users(self, brain_id: UUID) -> None:
        self.brain_user_repository.delete_brain_subscribers(
            brain_id=brain_id,
        )

    def create_brain_user(
        self, user_id: UUID, brain_id: UUID, rights: RoleEnum, is_default_brain: bool
    ):
        self.brain_user_repository.create_brain_user(
            user_id=user_id,
            brain_id=brain_id,
            rights=rights,
            default_brain=is_default_brain,
        )

    def get_brain_for_user(self, user_id: UUID, brain_id: UUID):
        return self.brain_user_repository.get_brain_for_user(user_id, brain_id)  # type: ignore

    def get_user_brains(self, user_id: UUID) -> list[MinimalUserBrainEntity]:
        results = self.brain_user_repository.get_user_brains(user_id)  # type: ignore

        return results  # type: ignore

    def get_brain_users(self, brain_id: UUID) -> List[BrainUser]:
        return self.brain_user_repository.get_brain_users(brain_id)

    def update_brain_user_rights(
        self, brain_id: UUID, user_id: UUID, rights: str
    ) -> None:
        self.brain_user_repository.update_brain_user_rights(
            brain_id=brain_id,
            user_id=user_id,
            rights=rights,
        )
