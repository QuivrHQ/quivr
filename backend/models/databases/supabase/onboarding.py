from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from models.databases.repository import Repository
from pydantic import BaseModel


class OnboardingUpdatableProperties(BaseModel):

    """Properties that can be received on onboarding update"""

    onboarding_a: Optional[bool]
    onboarding_b1: Optional[bool]
    onboarding_b2: Optional[bool]
    onboarding_b3: Optional[bool]

    class Config:
        extra = "forbid"


class OnboardingStates(BaseModel):
    """Response when getting onboarding"""

    onboarding_a: bool
    onboarding_b1: bool
    onboarding_b2: bool
    onboarding_b3: bool


class Onboarding(Repository):
    def __init__(self, supabase_client):
        self.db = supabase_client

    def get_user_onboarding(self, user_id: UUID) -> OnboardingStates | None:
        """
        Get user onboarding information by user_id
        """
        onboarding_data = (
            self.db.from_("onboardings")
            .select(
                "onboarding_a",
                "onboarding_b1",
                "onboarding_b2",
                "onboarding_b3",
            )
            .filter("user_id", "eq", user_id)
            .limit(1)
            .execute()
        ).data

        if onboarding_data == []:
            return None

        return OnboardingStates(**onboarding_data[0])

    def update_user_onboarding(
        self, user_id: UUID, onboarding: OnboardingUpdatableProperties
    ) -> OnboardingStates:
        """Update user onboarding information by user_id"""
        update_data = {
            key: value for key, value in onboarding.dict().items() if value is not None
        }

        response = (
            self.db.from_("onboardings")
            .update(update_data)
            .match({"user_id": user_id})
            .execute()
            .data
        )

        if not response:
            raise HTTPException(404, "User onboarding not updated")

        return OnboardingStates(**response[0])

    def remove_user_onboarding(self, user_id: UUID) -> OnboardingStates | None:
        """
        Remove user onboarding information by user_id
        """
        onboarding_data = (
            self.db.from_("onboardings")
            .delete()
            .match({"user_id": str(user_id)})
            .execute()
        ).data

        if onboarding_data == []:
            return None

        return OnboardingStates(**onboarding_data[0])

    def remove_onboarding_more_than_x_days(self, days: int):
        """
        Remove onboarding if it is older than x days
        """
        onboarding_data = (
            self.db.from_("onboardings")
            .delete()
            .lt(
                "creation_time",
                (datetime.now() - timedelta(days=days)).strftime(
                    "%Y-%m-%d %H:%M:%S.%f"
                ),
            )
            .execute()
        ).data

        return onboarding_data
