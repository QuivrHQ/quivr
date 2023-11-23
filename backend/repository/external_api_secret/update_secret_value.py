from uuid import UUID

from repository.external_api_secret.create_secret import create_secret
from repository.external_api_secret.delete_secret import delete_secret


def update_secret_value(
    user_id: UUID,
    brain_id: UUID,
    secret_name: str,
    secret_value: str,
) -> None:
    """Update an existing secret."""
    delete_secret(
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
