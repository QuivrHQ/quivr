from uuid import UUID

from fastapi import HTTPException
from models.brain_entity import BrainType
from models.settings import get_supabase_db

from repository.api_brain_definition.get_api_brain_definition import (
    get_api_brain_definition,
)
from repository.brain.get_brain_by_id import get_brain_by_id
from repository.external_api_secret.delete_secret import delete_secret


def delete_brain_user(user_id: UUID, brain_id: UUID) -> None:
    supabase_db = get_supabase_db()
    brain_to_delete_user_from = get_brain_by_id(brain_id=brain_id)
    if brain_to_delete_user_from is None:
        raise HTTPException(status_code=404, detail="Brain not found.")

    if brain_to_delete_user_from.brain_type == BrainType.API:
        brain_definition = get_api_brain_definition(brain_id=brain_id)
        if brain_definition is None:
            raise HTTPException(status_code=404, detail="Brain definition not found.")
        secrets = brain_definition.secrets
        for secret in secrets:
            delete_secret(
                user_id=user_id,
                brain_id=brain_id,
                secret_name=secret.name,
            )

    supabase_db.delete_brain_user_by_id(
        user_id=user_id,
        brain_id=brain_id,
    )
