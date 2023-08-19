import os
from uuid import UUID


def get_brain_url(origin: str, brain_id: UUID) -> str:
    """Generates the brain URL based on the brain_id."""

    return f"{origin}/invitation/{brain_id}"
