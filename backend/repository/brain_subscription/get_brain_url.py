import os
from uuid import UUID


def get_brain_url(brain_id: UUID) -> str:
    """Generates the brain URL based on the brain_id."""
    base_frontend_url = os.getenv("BASE_FRONTEND_URL")

    if not base_frontend_url:
        raise ValueError("BASE_FRONTEND_URL env variable is not defined for sending emails to share brains.")

    return f"{base_frontend_url}?brain_subscription_invitation={brain_id}"
