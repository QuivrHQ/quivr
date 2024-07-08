from quivr_core.api.modules.brain.entity.integration_brain import (
    IntegrationDescriptionEntity,
)
from quivr_core.api.modules.brain.repository.integration_brains import (
    IntegrationDescription,
)


class IntegrationBrainDescriptionService:

    def __init__(self):
        self.repository = IntegrationDescription()

    def get_all_integration_descriptions(self) -> list[IntegrationDescriptionEntity]:
        return self.repository.get_all_integration_descriptions()

    def get_integration_description(
        self, integration_id
    ) -> IntegrationDescriptionEntity | None:
        return self.repository.get_integration_description(integration_id)

    def get_integration_description_by_user_brain_id(
        self, brain_id, user_id
    ) -> IntegrationDescriptionEntity | None:
        return self.repository.get_integration_description_by_user_brain_id(
            brain_id, user_id
        )
