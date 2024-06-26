from uuid import UUID

from quivr_api.logger import get_logger
from quivr_api.models.brains_subscription_invitations import BrainSubscription
from quivr_api.models.settings import BrainSettings
from quivr_api.modules.brain.service.brain_service import BrainService
from quivr_api.packages.emails.send_email import send_email

logger = get_logger(__name__)

brain_service = BrainService()


def get_brain_url(origin: str, brain_id: UUID) -> str:
    """Generates the brain URL based on the brain_id."""

    return f"{origin}/invitation/{brain_id}"


def resend_invitation_email(
    brain_subscription: BrainSubscription,
    inviter_email: str,
    user_id: UUID,
    origin: str = "https://chat.quivr.app",
):
    brains_settings = BrainSettings()  # pyright: ignore reportPrivateUsage=none

    brain_url = get_brain_url(origin, brain_subscription.brain_id)

    invitation_brain = brain_service.get_brain_details(
        brain_subscription.brain_id, user_id
    )
    if invitation_brain is None:
        raise Exception("Brain not found")
    brain_name = invitation_brain.name

    html_body = f"""
    <p>Brain {brain_name} has been shared with you by {inviter_email}.</p>
    <p><a href='{brain_url}'>Click here</a> to access your brain.</p>
    """

    try:
        r = send_email(
            {
                "from": brains_settings.resend_email_address,
                "to": [brain_subscription.email],
                "subject": "Quivr - Brain Shared With You",
                "reply_to": "no-reply@quivr.app",
                "html": html_body,
            }
        )
        logger.info("Resend response", r)
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return

    return r
