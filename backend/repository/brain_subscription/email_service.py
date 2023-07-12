from typing import Optional
from uuid import UUID

import resend
from logger import get_logger
from models.brains_subscription_invitations import BrainSubscription

logger = get_logger(__name__)


class EmailService:
    def __init__(self, api_key: Optional[str]):
        if not api_key:
            raise ValueError("API key is not defined.")
        self.api_key = api_key

    def get_brain_url(self, brain_id: UUID) -> str:
        """Generates the brain URL based on the brain_id."""
        base_url = "https://www.quivr.app/"
        return f"{base_url}/invitation/{brain_id}"

    def resend_invitation_email(self, brain_subscription: BrainSubscription, inviter_email: str):
        resend.api_key = self.api_key

        brain_url = self.get_brain_url(brain_subscription.brain_id)

        html_body = f"""
        <p>This brain has been shared with you by {inviter_email}.</p>
        <p><a href='{brain_url}'>Click here</a> to access your brain.</p>
        """

        try:
            r = resend.Emails.send({
                "from": "onboarding@resend.dev",
                "to": brain_subscription.email,
                "subject": "Quivr - Brain Shared With You",
                "html": html_body
            })
            logger.info('Resend response', r)
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return

        return r
