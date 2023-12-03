from uuid import UUID

from modules.brain.service.brain_service import BrainService
from repository.external_api_secret.create_secret import create_secret

brain_service = BrainService()


def update_secret_value(
    user_id: UUID,
    brain_id: UUID,
    secret_name: str,
    secret_value: str,
) -> None:
    """Update an existing secret."""
    brain_service.delete_secret(
        user_id=user_id,
        brain_id=brain_id,
        secret_name=secret_name,
    )
    create_secret(
        user_id=user_id,
        brain_id=brain_id,
        secret_name=secret_name,
        secret_value=secret_value,
    )
