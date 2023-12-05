from uuid import UUID

from models import BrainEntity, get_supabase_client
from models.brain_entity import BrainType

from repository.api_brain_definition.get_api_brain_definition import (
    get_api_brain_definition,
)


def get_brain_details(brain_id: UUID) -> BrainEntity | None:
    supabase_client = get_supabase_client()
    response = (
        supabase_client.table("brains")
        .select("*")
        .filter("brain_id", "eq", str(brain_id))
        .execute()
    )
    if response.data == []:
        return None
    brain = BrainEntity(**response.data[0])

    if brain.brain_type == BrainType.API:
        brain_definition = get_api_brain_definition(brain_id)
        brain.brain_definition = brain_definition

    return brain
