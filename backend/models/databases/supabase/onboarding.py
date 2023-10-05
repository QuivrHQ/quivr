from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from models.databases.repository import (
    Repository,  # Assuming you have a repository class
)
from pydantic import BaseModel


class OnboardingUpdatableProperties(BaseModel):

    """Properties that can be received on onboarding update"""

    onboarding_b1: Optional[bool]
    onboarding_b2: Optional[bool]
    onboarding_b3: Optional[bool]


class GetOnboardingResponse(BaseModel):
    """Response when getting onboarding"""

    onboarding_b1: bool
    onboarding_b2: bool
    onboarding_b3: bool


class Onboarding(Repository):
    def __init__(self, supabase_client):
        self.db = supabase_client

    def get_user_onboarding(self, user_id: UUID) -> GetOnboardingResponse | None:
        """
        Get user onboarding information by user_id
        """
        onboarding_data = (
            self.db.from_("onboarding")
            .select("user_id", "onboarding_b1", "onboarding_b2", "onboarding_b3")
            .filter("user_id", "eq", user_id)
            .limit(1)
            .execute()
        ).data

        if onboarding_data == []:
            return None

        return GetOnboardingResponse(**onboarding_data[0])

    def update_user_onboarding(
        self, user_id: UUID, onboarding: OnboardingUpdatableProperties
    ) -> GetOnboardingResponse:
        """Update user onboarding information by user_id"""
        response = (
            self.db.from_("onboarding")
            .update(onboarding.dict())
            .match({"user_id": user_id})
            .execute()
            .data
        )

        if not response:
            raise HTTPException(404, "User onboarding not updated")

        return GetOnboardingResponse(**response[0])
