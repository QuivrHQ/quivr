from uuid import UUID

from logger import get_logger
from models.settings import get_supabase_client
from pydantic import BaseModel
from supabase.client import Client

logger = get_logger(__name__)


class BrainSubscription(BaseModel):
    brain_id: UUID
    email: str
    rights: str = "Viewer"

    class Config:
        arbitrary_types_allowed = True

    @property
    def supabase_client(self) -> Client:
        return get_supabase_client()

    def create_subscription_invitation(self):
        logger.info("Creating subscription invitation")
        response = (
            self.supabase_client.table("brain_subscription_invitations")
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
            self.supabase_client.table("brain_subscription_invitations")
            .update({"rights": self.rights})
            .eq("brain_id", str(self.brain_id))
            .eq("email", self.email)
            .execute()
        )
        return response.data

    def create_or_update_subscription_invitation(self):
        response = (
            self.supabase_client.table("brain_subscription_invitations")
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
