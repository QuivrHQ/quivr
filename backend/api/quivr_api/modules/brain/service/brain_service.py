from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from quivr_api.celery_config import celery
from quivr_api.logger import get_logger
from quivr_api.modules.brain.dto.inputs import (
    BrainUpdatableProperties,
    CreateBrainProperties,
)
from quivr_api.modules.brain.entity.brain_entity import (
    BrainEntity,
    BrainType,
    PublicBrain,
)
from quivr_api.modules.brain.entity.integration_brain import IntegrationEntity
from quivr_api.modules.brain.repository import (
    Brains,
    BrainsUsers,
    BrainsVectors,
    IntegrationBrain,
    IntegrationDescription,
)
from quivr_api.modules.brain.service.api_brain_definition_service import (
    ApiBrainDefinitionService,
)
from quivr_api.modules.brain.service.utils.validate_brain import validate_api_brain
from quivr_api.modules.knowledge.service.knowledge_service import KnowledgeService
from quivr_api.vectorstore.supabase import CustomSupabaseVectorStore

logger = get_logger(__name__)

knowledge_service = KnowledgeService()
api_brain_definition_service = ApiBrainDefinitionService()


class BrainService:
    # brain_repository: BrainsInterface
    # brain_user_repository: BrainsUsersInterface
    # brain_vector_repository: BrainsVectorsInterface
    # external_api_secrets_repository: ExternalApiSecretsInterface
    # integration_brains_repository: IntegrationBrainInterface
    # integration_description_repository: IntegrationDescriptionInterface

    def __init__(self):
        self.brain_repository: Brains = Brains()
        self.brain_user_repository = BrainsUsers()
        self.brain_vector = BrainsVectors()
        self.integration_brains_repository = IntegrationBrain()
        self.integration_description_repository = IntegrationDescription()

    def get_brain_by_id(self, brain_id: UUID):
        return self.brain_repository.get_brain_by_id(brain_id)

    def get_integration_brain(self, brain_id) -> IntegrationEntity | None:
        return self.integration_brains_repository.get_integration_brain(brain_id)

    def find_brain_from_question(
        self,
        brain_id: UUID,
        question: str,
        user,
        chat_id: UUID,
        history,
        vector_store: CustomSupabaseVectorStore,
    ) -> (Optional[BrainEntity], dict[str, str]):
        """Find the brain to use for a question.

        Args:
            brain_id (UUID): ID of the brain to use if exists
            question (str): Question for which to find the brain
            user (UserEntity): User asking the question
            chat_id (UUID): ID of the chat

        Returns:
            Optional[BrainEntity]: Returns the brain to use for the question
        """
        metadata = {}

        # Init

        brain_id_to_use = brain_id
        brain_to_use = None

        # Get the first question from the chat_question

        question = question

        list_brains = []  # To return

        if history and not brain_id_to_use:
            question = history[0].user_message
            brain_id_to_use = history[0].brain_id
            brain_to_use = self.get_brain_by_id(brain_id_to_use)

        # If a brain_id is provided, use it
        if brain_id_to_use and not brain_to_use:
            brain_to_use = self.get_brain_by_id(brain_id_to_use)

        else:
            # Calculate the closest brains to the question
            list_brains = vector_store.find_brain_closest_query(user.id, question)

            unique_list_brains = []
            seen_brain_ids = set()

            for brain in list_brains:
                if brain["id"] not in seen_brain_ids:
                    unique_list_brains.append(brain)
                    seen_brain_ids.add(brain["id"])

            metadata["close_brains"] = unique_list_brains[:5]

            if list_brains and not brain_to_use:
                brain_id_to_use = list_brains[0]["id"]
                brain_to_use = self.get_brain_by_id(brain_id_to_use)

        return brain_to_use, metadata

    def create_brain(
        self,
        user_id: UUID,
        brain: Optional[CreateBrainProperties],
    ) -> BrainEntity:
        if brain is None:
            brain = CreateBrainProperties()  # type: ignore model and brain_definition

        if brain.brain_type == BrainType.api:
            validate_api_brain(brain)
            return self.create_brain_api(user_id, brain)

        if brain.brain_type == BrainType.composite:
            return self.create_brain_composite(brain)

        if brain.brain_type == BrainType.integration:
            return self.create_brain_integration(user_id, brain)

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

    def create_brain_integration(
        self,
        user_id: UUID,
        brain: CreateBrainProperties,
    ) -> BrainEntity:
        created_brain = self.brain_repository.create_brain(brain)
        if brain.integration is not None:
            self.integration_brains_repository.add_integration_brain(
                user_id=user_id,
                brain_id=created_brain.brain_id,
                integration_id=brain.integration.integration_id,
                settings=brain.integration.settings,
            )
        if (
            self.integration_description_repository.get_integration_description(
                brain.integration.integration_id
            ).integration_name.lower()
            == "notion"
        ):
            celery.send_task(
                "NotionConnectorLoad",
                kwargs={"brain_id": created_brain.brain_id, "user_id": user_id},
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

        if brain_to_delete.brain_type == BrainType.api:
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
                    exclude={"brain_definition", "connected_brains_ids", "integration"}
                )
            ),
        )

        if brain_update_answer is None:
            raise HTTPException(
                status_code=404,
                detail=f"Brain with id {brain_id} not found",
            )

        if (
            brain_update_answer.brain_type == BrainType.api
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

    def get_brain_details(
        self, brain_id: UUID, user_id: UUID = None
    ) -> BrainEntity | None:
        brain = self.brain_repository.get_brain_details(brain_id)
        if brain is None:
            return None

        # TODO: N+1 here !!
        if brain.brain_type == BrainType.integration:
            brain.integration = (
                self.integration_brains_repository.get_integration_brain(
                    brain_id, user_id
                )
            )

            if brain.integration:
                brain.integration_description = (
                    self.integration_description_repository.get_integration_description(
                        brain.integration.integration_id
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
