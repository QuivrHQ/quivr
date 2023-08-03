from uuid import UUID

from models.brain_entity import BrainEntity
from models.settings import common_dependencies


def get_brain_details(brain_id: UUID) -> BrainEntity | None:
    commons = common_dependencies()
    response = (
        commons["supabase"]
        .from_("brains")
        .select("*")
        .filter("brain_id", "eq", brain_id)
        .execute()
    )
    if response.data == []:
        return None

    return BrainEntity(**response.data[0])
