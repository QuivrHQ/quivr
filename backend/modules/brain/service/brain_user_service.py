from uuid import UUID

from fastapi import HTTPException
from modules.brain.entity.brain_entity import BrainType
from modules.brain.repository.brains import Brain
from modules.brain.repository.interfaces.brains_users_interface import (
    BrainsUsersInterface,
)
from modules.brain.service.brain_service import BrainService
from repository.api_brain_definition.get_api_brain_definition import (
    get_api_brain_definition,
)
from repository.external_api_secret.delete_secret import delete_secret

brain_service = BrainService()


class BrainUserService:
    brain_user_repository: BrainsUsersInterface

    def __init__(self):
        self.brain_repository = Brain()

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
