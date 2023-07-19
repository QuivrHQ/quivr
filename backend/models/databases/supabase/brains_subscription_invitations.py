from models.databases.repository import Repository

from logger import get_logger

logger = get_logger(__name__)


class BrainSubscription(Repository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create_subscription_invitation(self, brain_id, user_email, rights):
        logger.info("Creating subscription invitation")
        response = (
            self.db.table("brain_subscription_invitations")
            .insert({"brain_id": str(brain_id), "email": user_email, "rights": rights})
            .execute()
        )
        return response.data

    def update_subscription_invitation(self, brain_id, user_email, rights):
        logger.info("Updating subscription invitation")
        response = (
            self.db.table("brain_subscription_invitations")
            .update({"rights": rights})
            .eq("brain_id", str(brain_id))
            .eq("email", user_email)
            .execute()
        )
        return response.data

    def create_or_update_subscription_invitation(self, brain_id, user_email):
        response = (
            self.db.table("brain_subscription_invitations")
            .select("*")
            .eq("brain_id", str(brain_id))
            .eq("email", user_email)
            .execute()
        )
        if response.data:
            response = self.update_subscription_invitation()
        else:
            response = self.create_subscription_invitation()

        return response
