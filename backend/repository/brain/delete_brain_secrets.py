from uuid import UUID

from fastapi import HTTPException
from models.settings import get_supabase_db

from repository.api_brain_definition.get_api_brain_definition import (
    get_api_brain_definition,
)
from repository.external_api_secret import delete_secret


def delete_brain_secrets_values(brain_id: UUID) -> None:
    supabase_db = get_supabase_db()

    brain_definition = get_api_brain_definition(brain_id=brain_id)

    if brain_definition is None:
        raise HTTPException(status_code=404, detail="Brain definition not found.")

    secrets = brain_definition.secrets

    if len(secrets) > 0:
        brain_users = supabase_db.get_brain_users(brain_id=brain_id)
        for user in brain_users:
            for secret in secrets:
                delete_secret(
                    user_id=user.user_id,
                    brain_id=brain_id,
                    secret_name=secret.name,
                )
