from uuid import UUID

from quivr_api.modules.onboarding.dto.inputs import OnboardingUpdatableProperties
from quivr_api.modules.onboarding.entity.onboarding import OnboardingStates
from quivr_api.modules.onboarding.repository.onboardings import Onboarding
from quivr_api.modules.onboarding.repository.onboardings_interface import (
    OnboardingInterface,
)


class OnboardingService:
    repository: OnboardingInterface

    def __init__(self):
        self.repository = Onboarding()

    def create_user_onboarding(self, user_id: UUID) -> OnboardingStates:
        """Update user onboarding information by user_id"""

        return self.repository.create_user_onboarding(user_id)

    def get_user_onboarding(self, user_id: UUID) -> OnboardingStates | None:
        """
        Get a user's onboarding status

        Args:
            user_id (UUID): The id of the user

        Returns:
            Onboardings: The user's onboarding status
        """
        return self.repository.get_user_onboarding(user_id)

    def remove_onboarding_more_than_x_days(self, days: int):
        """
        Remove onboarding if it is older than x days
        """

        self.repository.remove_onboarding_more_than_x_days(days)

    def update_user_onboarding(
        self, user_id: UUID, onboarding: OnboardingUpdatableProperties
    ) -> OnboardingStates:
        """Update user onboarding information by user_id"""

        updated_onboarding = self.repository.update_user_onboarding(user_id, onboarding)

        if all(not value for value in updated_onboarding.dict().values()):
            self.repository.remove_user_onboarding(user_id)

        return updated_onboarding
