from abc import ABC, abstractmethod
from uuid import UUID

from modules.onboarding.dto.inputs import OnboardingUpdatableProperties
from modules.onboarding.entity.onboarding import OnboardingStates


class OnboardingInterface(ABC):
    @abstractmethod
    def get_user_onboarding(self, user_id: UUID) -> OnboardingStates | None:
        """
        Get user onboarding information by user_id
        """
        pass

    @abstractmethod
    def update_user_onboarding(
        self, user_id: UUID, onboarding: OnboardingUpdatableProperties
    ) -> OnboardingStates:
        """Update user onboarding information by user_id"""
        pass

    @abstractmethod
    def remove_user_onboarding(self, user_id: UUID) -> OnboardingStates | None:
        """
        Remove user onboarding information by user_id
        """
        pass

    @abstractmethod
    def create_user_onboarding(self, user_id: UUID) -> OnboardingStates:
        """
        Create user onboarding information by user_id
        """
        pass

    @abstractmethod
    def remove_onboarding_more_than_x_days(self, days: int):
        """
        Remove onboarding if it is older than x days
        """
        """Update a prompt by id"""
        pass
