import os
from typing import Optional
from uuid import UUID

import resend
from logger import get_logger
from models.settings import CommonsDep, common_dependencies
from pydantic import BaseModel

logger = get_logger(__name__)


class BrainSubscription(BaseModel):
    brain_id: Optional[UUID] = None
    inviter_email: Optional[str]
    email: Optional[str]
    rights: Optional[str]

    class Config:
        arbitrary_types_allowed = True

    @property
    def commons(self) -> CommonsDep:
        return common_dependencies()

    def create_subscription_invitation(self):
        return self.commons["db"].create_subscription_invitation(self.brain_id, self.email, self.rights)

    def update_subscription_invitation(self):
        return self.commons["db"].update_subscription_invitation(self.brain_id, self.email, self.rights)

    def create_or_update_subscription_invitation(self):
        return self.commons["db"].create_or_update_subscription_invitation(self.brain_id, self.email)

    def get_brain_url(self) -> str:
        """Generates the brain URL based on the brain_id."""
        base_url = "https://www.quivr.app/chat"
        return f"{base_url}?brain_subscription_invitation={self.brain_id}"

    def resend_invitation_email(self):
        resend.api_key = os.getenv("RESEND_API_KEY")

        brain_url = self.get_brain_url()

        html_body = f"""
        <p>This brain has been shared with you by {self.inviter_email}.</p>
        <p><a href='{brain_url}'>Click here</a> to access your brain.</p>
        """

        try:
            r = resend.Emails.send({
                "from": "onboarding@resend.dev",
                "to": self.email,
                "subject": "Quivr - Brain Shared With You",
                "html": html_body
            })
            print('Resend response', r)
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return

        return r
