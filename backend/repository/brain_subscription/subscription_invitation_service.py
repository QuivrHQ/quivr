from typing import Optional

from logger import get_logger
from models.brains_subscription_invitations import BrainSubscription
from models.settings import CommonsDep, common_dependencies

logger = get_logger(__name__)


class SubscriptionInvitationService:
    def __init__(self, commons: Optional[CommonsDep] = None):
        self.commons = commons if commons else common_dependencies()

    def create_subscription_invitation(self, brain_subscription: BrainSubscription):
        logger.info("Creating subscription invitation")
        response = (
            self.commons["supabase"]
            .table("brain_subscription_invitations")
            .insert({"brain_id": str(brain_subscription.brain_id), "email": brain_subscription.email, "rights": brain_subscription.rights})
            .execute()
        )
        return response.data

    def update_subscription_invitation(self, brain_subscription: BrainSubscription):
        logger.info('Updating subscription invitation')
        response = (
            self.commons["supabase"]
            .table("brain_subscription_invitations")
            .update({"rights": brain_subscription.rights})
            .eq("brain_id", str(brain_subscription.brain_id))
            .eq("email", brain_subscription.email)
            .execute()
        )
        return response.data

    def create_or_update_subscription_invitation(self, brain_subscription: BrainSubscription):
        response = self.commons["supabase"].table("brain_subscription_invitations").select("*").eq("brain_id", str(brain_subscription.brain_id)).eq("email", brain_subscription.email).execute()

        if response.data:
            response = self.update_subscription_invitation(brain_subscription)
        else:
           response = self.create_subscription_invitation(brain_subscription)

        return response
