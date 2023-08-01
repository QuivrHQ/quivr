from typing import Optional

from logger import get_logger
from models.brains_subscription_invitations import BrainSubscription
from models.settings import CommonsDep, get_supabase_client
from utils.db_commands import (
    delete_data_in_table,
    insert_data_in_table,
    select_data_in_table,
    update_data_in_table,
)

logger = get_logger(__name__)


class SubscriptionInvitationService:
    def __init__(self, commons: Optional[CommonsDep] = None):
        self.supabase_client = get_supabase_client()

    def create_subscription_invitation(self, brain_subscription: BrainSubscription):
        logger.info("Creating subscription invitation")
        data = {
            "brain_id": str(brain_subscription.brain_id),
            "email": brain_subscription.email,
            "rights": brain_subscription.rights,
        }
        response_data = insert_data_in_table(
            supabase_client=self.supabase_client,
            table_name="brain_subscription_invitations",
            data=data,
            message="Creating subscription invitation",
        )

        return response_data

    def update_subscription_invitation(self, brain_subscription: BrainSubscription):
        logger.info("Updating subscription invitation")
        response_data = update_data_in_table(
            supabase_client=self.supabase_client,
            table_name="brain_subscription_invitations",
            data={"rights": brain_subscription.rights},
            identifier={
                "brain_id": str(brain_subscription.brain_id),
                "email": brain_subscription.email,
            },
        )
        return response_data

    def create_or_update_subscription_invitation(
        self, brain_subscription: BrainSubscription
    ):
        response_data = select_data_in_table(
            supabase_client=self.supabase_client,
            table_name="brain_subscription_invitations",
            identifier={
                "brain_id": str(brain_subscription.brain_id),
                "email": brain_subscription.email,
            },
        )

        if response_data:
            response = self.update_subscription_invitation(brain_subscription)
        else:
            response = self.create_subscription_invitation(brain_subscription)

        return response

    def fetch_invitation(self, subscription: BrainSubscription):
        logger.info("Fetching subscription invitation")
        response_data = select_data_in_table(
            supabase_client=self.supabase_client,
            table_name="brain_subscription_invitations",
            identifier={
                "brain_id": str(subscription.brain_id),
                "email": subscription.email,
            },
        )
        if response_data.data:
            return response_data[0]  # return the first matching invitation
        else:
            return None

    def remove_invitation(self, subscription: BrainSubscription):
        logger.info(
            f"Removing subscription invitation for email {subscription.email} and brain {subscription.brain_id}"
        )
        response_data = delete_data_in_table(
            supabase_client=self.supabase_client,
            table_name="brain_subscription_invitations",
            identifier={
                "brain_id": str(subscription.brain_id),
                "email": subscription.email,
            },
        )
        logger.info(
            f"Removed subscription invitation for email {subscription.email} and brain {subscription.brain_id}"
        )
        logger.info(response_data)
        return response_data
