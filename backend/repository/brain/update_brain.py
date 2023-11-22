from uuid import UUID

from fastapi import HTTPException
from models import BrainEntity, get_supabase_db
from models.brain_entity import BrainType
from models.databases.supabase.brains import BrainUpdatableProperties

from repository.api_brain_definition.update_api_brain_definition import (
    update_api_brain_definition,
)
from repository.brain.update_brain_last_update_time import update_brain_last_update_time


def update_brain_by_id(
    brain_id: UUID, brain_new_values: BrainUpdatableProperties
) -> BrainEntity:
    """Update a prompt by id"""
    supabase_db = get_supabase_db()

    existing_brain = supabase_db.get_brain_by_id(brain_id)

    if existing_brain is None:
        raise HTTPException(
            status_code=404,
            detail=f"Brain with id {brain_id} not found",
        )

    brain_update_answer = supabase_db.update_brain_by_id(
        brain_id,
        brain=BrainUpdatableProperties(
            **brain_new_values.dict(exclude={"brain_definition"})
        ),
    )

    if brain_update_answer is None:
        raise HTTPException(
            status_code=404,
            detail=f"Brain with id {brain_id} not found",
        )

    if (
        brain_update_answer.brain_type == BrainType.API
        and brain_new_values.brain_definition
    ):
        if existing_brain.brain_definition and existing_brain.brain_definition.secrets:
            brain_new_values.brain_definition.secrets = (
                existing_brain.brain_definition.secrets
            )
        else:
            brain_new_values.brain_definition.secrets = []

        update_api_brain_definition(
            brain_id,
            api_brain_definition=brain_new_values.brain_definition,
        )

    if brain_update_answer is None:
        raise HTTPException(
            status_code=404,
            detail=f"Brain with id {brain_id} not found",
        )

    update_brain_last_update_time(brain_id)
    return brain_update_answer
