from uuid import UUID

from logger import get_logger
from pydantic import BaseModel

from models.settings import CommonsDep, common_dependencies

logger = get_logger(__name__)


class BrainSubscription(BaseModel):
    brain_id: UUID
    email: str
    rights: str = "Viewer"

    class Config:
        arbitrary_types_allowed = True

    @property
    def commons(self) -> CommonsDep:
        return common_dependencies()

    def create_subscription_invitation(self):
        logger.info("Creating subscription invitation")
        response = (
            self.commons["supabase"]
            .table("brain_subscription_invitations")
            .insert(
                {
                    "brain_id": str(self.brain_id),
                    "email": self.email,
                    "rights": self.rights,
                }
            )
            .execute()
        )
        return response.data

    def update_subscription_invitation(self):
        logger.info("Updating subscription invitation")
        response = (
            self.commons["supabase"]
            .table("brain_subscription_invitations")
            .update({"rights": self.rights})
            .eq("brain_id", str(self.brain_id))
            .eq("email", self.email)
            .execute()
        )
        return response.data

    def create_or_update_subscription_invitation(self):
        response = (
            self.commons["supabase"]
            .table("brain_subscription_invitations")
            .select("*")
            .eq("brain_id", str(self.brain_id))
            .eq("email", self.email)
            .execute()
        )

        if response.data:
            response = self.update_subscription_invitation()
        else:
            response = self.create_subscription_invitation()

        return response
