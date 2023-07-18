import resend
from logger import get_logger
from models.brains_subscription_invitations import BrainSubscription
from models.settings import BrainSettings
from repository.brain_subscription.get_brain_url import get_brain_url

logger = get_logger(__name__)


def resend_invitation_email(brain_subscription: BrainSubscription, inviter_email: str, origin: str = "https://www.quivr.app"):
    brains_settings = BrainSettings()  # pyright: ignore reportPrivateUsage=none
    resend.api_key = brains_settings.resend_api_key

    brain_url = get_brain_url(origin, brain_subscription.brain_id)

    html_body = f"""
    <p>This brain has been shared with you by {inviter_email}.</p>
    <p><a href='{brain_url}'>Click here</a> to access your brain.</p>
    """

    try:
        r = resend.Emails.send({
            "from": brains_settings.resend_email_address,
            "to": brain_subscription.email,
            "subject": "Quivr - Brain Shared With You",
            "html": html_body
        })
        logger.info('Resend response', r)
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return

    return r
