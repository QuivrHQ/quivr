from datetime import datetime, timedelta

from fastapi import HTTPException
from models.settings import get_supabase_client
from modules.onboarding.entity.onboarding import OnboardingStates

from .onboardings_interface import OnboardingInterface


class Onboarding(OnboardingInterface):
    def __init__(self):
        supabase_client = get_supabase_client()
        self.db = supabase_client

    def get_user_onboarding(self, user_id):
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

    def update_user_onboarding(self, user_id, onboarding):
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

    def remove_user_onboarding(self, user_id):
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

    def create_user_onboarding(self, user_id):
        """
        Create user onboarding information by user_id
        """
        onboarding_data = (
            self.db.from_("onboardings")
            .insert(
                [
                    {
                        "user_id": str(user_id),
                    }
                ]
            )
            .execute()
        ).data

        return OnboardingStates(**onboarding_data[0])

    def remove_onboarding_more_than_x_days(self, days):
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
