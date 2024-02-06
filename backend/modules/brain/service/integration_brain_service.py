from modules.brain.entity.integration_brain import IntegrationDescriptionEntity
from modules.brain.repository.integration_brains import IntegrationDescription
from modules.brain.repository.interfaces import IntegrationDescriptionInterface


class IntegrationBrainDescriptionService:
    repository: IntegrationDescriptionInterface

    def __init__(self):
        self.repository = IntegrationDescription()

    def get_all_integration_descriptions(self) -> list[IntegrationDescriptionEntity]:
        return self.repository.get_all_integration_descriptions()

    def get_integration_description(
        self, integration_id
    ) -> IntegrationDescriptionEntity:
        return self.repository.get_integration_description(integration_id)

    def get_integration_description_by_user_brain_id(
        self, brain_id, user_id
    ) -> IntegrationDescriptionEntity:
        return self.repository.get_integration_description_by_user_brain_id(
            brain_id, user_id
        )
