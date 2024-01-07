from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from modules.brain.dto.inputs import BrainUpdatableProperties, CreateBrainProperties
from modules.brain.entity.brain_entity import BrainEntity, BrainType, PublicBrain
from modules.brain.repository import (
    Brains,
    BrainsUsers,
    BrainsVectors,
    CompositeBrainsConnections,
    ExternalApiSecrets,
)
from modules.brain.repository.interfaces import (
    BrainsInterface,
    BrainsUsersInterface,
    BrainsVectorsInterface,
    CompositeBrainsConnectionsInterface,
    ExternalApiSecretsInterface,
)
from modules.brain.service.api_brain_definition_service import ApiBrainDefinitionService
from modules.brain.service.utils.validate_brain import validate_api_brain
from modules.knowledge.service.knowledge_service import KnowledgeService

knowledge_service = KnowledgeService()
# TODO: directly user api_brain_definition repository
api_brain_definition_service = ApiBrainDefinitionService()


class BrainService:
    brain_repository: BrainsInterface
    brain_user_repository: BrainsUsersInterface
    brain_vector_repository: BrainsVectorsInterface
    external_api_secrets_repository: ExternalApiSecretsInterface
    composite_brains_connections_repository: CompositeBrainsConnectionsInterface

    def __init__(self):
        self.brain_repository = Brains()
        self.brain_user_repository = BrainsUsers()
        self.brain_vector = BrainsVectors()
        self.external_api_secrets_repository = ExternalApiSecrets()
        self.composite_brains_connections_repository = CompositeBrainsConnections()

    def get_brain_by_id(self, brain_id: UUID):
        return self.brain_repository.get_brain_by_id(brain_id)

    def create_brain(
        self,
        user_id: UUID,
        brain: Optional[CreateBrainProperties],
    ) -> BrainEntity:
        if brain == None:
            brain = CreateBrainProperties()  # type: ignore model and brain_definition

        if brain.brain_type == BrainType.API:
            validate_api_brain(brain)
            return self.create_brain_api(user_id, brain)

        if brain.brain_type == BrainType.COMPOSITE:
            return self.create_brain_composite(brain)

        created_brain = self.brain_repository.create_brain(brain)
        return created_brain

    def create_brain_api(
        self,
        user_id: UUID,
        brain: CreateBrainProperties,
    ) -> BrainEntity:
        created_brain = self.brain_repository.create_brain(brain)

        if brain.brain_definition is not None:
            api_brain_definition_service.add_api_brain_definition(
                brain_id=created_brain.brain_id,
                api_brain_definition=brain.brain_definition,
            )

        secrets_values = brain.brain_secrets_values

        for secret_name in secrets_values:
            self.external_api_secrets_repository.create_secret(
                user_id=user_id,
                brain_id=created_brain.brain_id,
                secret_name=secret_name,
                secret_value=secrets_values[secret_name],
            )

        return created_brain

    def create_brain_composite(
        self,
        brain: CreateBrainProperties,
    ) -> BrainEntity:
        created_brain = self.brain_repository.create_brain(brain)

        if brain.connected_brains_ids is not None:
            for connected_brain_id in brain.connected_brains_ids:
                self.composite_brains_connections_repository.connect_brain(
                    composite_brain_id=created_brain.brain_id,
                    connected_brain_id=connected_brain_id,
                )

        return created_brain

    def delete_brain_secrets_values(self, brain_id: UUID) -> None:
        brain_definition = api_brain_definition_service.get_api_brain_definition(
            brain_id=brain_id
        )

        if brain_definition is None:
            raise HTTPException(status_code=404, detail="Brain definition not found.")

        secrets = brain_definition.secrets

        if len(secrets) > 0:
            brain_users = self.brain_user_repository.get_brain_users(brain_id=brain_id)
            for user in brain_users:
                for secret in secrets:
                    self.external_api_secrets_repository.delete_secret(
                        user_id=user.user_id,
                        brain_id=brain_id,
                        secret_name=secret.name,
                    )

    def delete_brain(self, brain_id: UUID) -> dict[str, str]:
        brain_to_delete = self.get_brain_by_id(brain_id=brain_id)
        if brain_to_delete is None:
            raise HTTPException(status_code=404, detail="Brain not found.")

        if brain_to_delete.brain_type == BrainType.API:
            self.delete_brain_secrets_values(
                brain_id=brain_id,
            )
            api_brain_definition_service.delete_api_brain_definition(brain_id=brain_id)
        else:
            knowledge_service.remove_brain_all_knowledge(brain_id)

        self.brain_vector.delete_brain_vector(str(brain_id))
        self.brain_user_repository.delete_brain_users(str(brain_id))
        self.brain_repository.delete_brain(str(brain_id))  # type: ignore

        return {"message": "Brain deleted."}

    def get_brain_prompt_id(self, brain_id: UUID) -> UUID | None:
        brain = self.get_brain_by_id(brain_id)
        prompt_id = brain.prompt_id if brain else None

        return prompt_id

    def update_brain_by_id(
        self, brain_id: UUID, brain_new_values: BrainUpdatableProperties
    ) -> BrainEntity:
        """Update a prompt by id"""

        existing_brain = self.brain_repository.get_brain_by_id(brain_id)

        if existing_brain is None:
            raise HTTPException(
                status_code=404,
                detail=f"Brain with id {brain_id} not found",
            )

        brain_update_answer = self.brain_repository.update_brain_by_id(
            brain_id,
            brain=BrainUpdatableProperties(
                **brain_new_values.dict(
                    exclude={"brain_definition", "connected_brains_ids"}
                )
            ),
        )

        if brain_update_answer is None:
            raise HTTPException(
                status_code=404,
                detail=f"Brain with id {brain_id} not found",
            )

        if (
            brain_update_answer.brain_type == BrainType.API
            and brain_new_values.brain_definition
        ):
            existing_brain_secrets_definition = (
                existing_brain.brain_definition.secrets
                if existing_brain.brain_definition
                else None
            )
            brain_new_values_secrets_definition = (
                brain_new_values.brain_definition.secrets
                if brain_new_values.brain_definition
                else None
            )
            should_remove_existing_secrets_values = (
                existing_brain_secrets_definition
                and brain_new_values_secrets_definition
                and existing_brain_secrets_definition
                != brain_new_values_secrets_definition
            )

            if should_remove_existing_secrets_values:
                self.delete_brain_secrets_values(brain_id=brain_id)

            api_brain_definition_service.update_api_brain_definition(
                brain_id,
                api_brain_definition=brain_new_values.brain_definition,
            )

        if brain_update_answer is None:
            raise HTTPException(
                status_code=404,
                detail=f"Brain with id {brain_id} not found",
            )

        self.brain_repository.update_brain_last_update_time(brain_id)
        return brain_update_answer

    def update_brain_last_update_time(self, brain_id: UUID):
        self.brain_repository.update_brain_last_update_time(brain_id)

    def get_brain_details(self, brain_id: UUID) -> BrainEntity | None:
        brain = self.brain_repository.get_brain_details(brain_id)
        if brain == None:
            return None

        if brain.brain_type == BrainType.API:
            brain_definition = api_brain_definition_service.get_api_brain_definition(
                brain_id
            )
            brain.brain_definition = brain_definition

        if brain.brain_type == BrainType.COMPOSITE:
            brain.connected_brains_ids = (
                self.composite_brains_connections_repository.get_connected_brains(
                    brain_id
                )
            )
        return brain

    def get_connected_brains(self, brain_id: UUID) -> list[BrainEntity]:
        return self.composite_brains_connections_repository.get_connected_brains(
            brain_id
        )

    def get_public_brains(self) -> list[PublicBrain]:
        return self.brain_repository.get_public_brains()

    def update_secret_value(
        self,
        user_id: UUID,
        brain_id: UUID,
        secret_name: str,
        secret_value: str,
    ) -> None:
        """Update an existing secret."""
        self.external_api_secrets_repository.delete_secret(
            user_id=user_id,
            brain_id=brain_id,
            secret_name=secret_name,
        )
        self.external_api_secrets_repository.create_secret(
            user_id=user_id,
            brain_id=brain_id,
            secret_name=secret_name,
            secret_value=secret_value,
        )
