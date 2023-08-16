from uuid import UUID

from models import BrainEntity, get_supabase_client


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
    return BrainEntity(**response.data[0])
