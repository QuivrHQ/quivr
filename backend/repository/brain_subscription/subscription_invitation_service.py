from logger import get_logger
from models import BrainSubscription, get_supabase_client
from modules.brain.service.brain_user_service import BrainUserService
from modules.user.service.user_service import UserService

logger = get_logger(__name__)


brain_user_service = BrainUserService()
user_service = UserService()


class SubscriptionInvitationService:
    def __init__(self):
        self.supabase_client = get_supabase_client()

    def create_subscription_invitation(self, brain_subscription: BrainSubscription):
        logger.info("Creating subscription invitation")
        response = (
            self.supabase_client.table("brain_subscription_invitations")
            .insert(
                {
                    "brain_id": str(brain_subscription.brain_id),
                    "email": brain_subscription.email,
                    "rights": brain_subscription.rights,
                }
            )
            .execute()
        )
        return response.data

    def update_subscription_invitation(self, brain_subscription: BrainSubscription):
        logger.info("Updating subscription invitation")
        response = (
            self.supabase_client.table("brain_subscription_invitations")
            .update({"rights": brain_subscription.rights})
            .eq("brain_id", str(brain_subscription.brain_id))
            .eq("email", brain_subscription.email)
            .execute()
        )
        return response.data

    def create_or_update_subscription_invitation(
        self,
        brain_subscription: BrainSubscription,
    ) -> bool:
        """
        Creates a subscription invitation if it does not exist, otherwise updates it.
        Returns True if the invitation was created or updated and False if user already has access.
        """
        response = (
            self.supabase_client.table("brain_subscription_invitations")
            .select("*")
            .eq("brain_id", str(brain_subscription.brain_id))
            .eq("email", brain_subscription.email)
            .execute()
        )

        if response.data:
            self.update_subscription_invitation(brain_subscription)
            return True
        else:
            user_id = user_service.get_user_id_by_email(brain_subscription.email)
            brain_user = None

            if user_id is not None:
                brain_id = brain_subscription.brain_id
                brain_user = brain_user_service.get_brain_for_user(user_id, brain_id)

            if brain_user is None:
                self.create_subscription_invitation(brain_subscription)
                return True

        return False

    def fetch_invitation(self, subscription: BrainSubscription):
        logger.info("Fetching subscription invitation")
        response = (
            self.supabase_client.table("brain_subscription_invitations")
            .select("*")
            .eq("brain_id", str(subscription.brain_id))
            .eq("email", subscription.email)
            .execute()
        )
        if response.data:
            return response.data[0]  # return the first matching invitation
        else:
            return None

    def remove_invitation(self, subscription: BrainSubscription):
        logger.info(
            f"Removing subscription invitation for email {subscription.email} and brain {subscription.brain_id}"
        )
        response = (
            self.supabase_client.table("brain_subscription_invitations")
            .delete()
            .eq("brain_id", str(subscription.brain_id))
            .eq("email", subscription.email)
            .execute()
        )
        logger.info(
            f"Removed subscription invitation for email {subscription.email} and brain {subscription.brain_id}"
        )
        logger.info(response)
        return response.data
