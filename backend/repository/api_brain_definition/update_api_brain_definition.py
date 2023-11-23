from typing import Optional
from uuid import UUID

from models.ApiBrainDefinition import ApiBrainDefinition
from models.settings import get_supabase_db


def update_api_brain_definition(
    brain_id: UUID, api_brain_definition: ApiBrainDefinition
) -> Optional[ApiBrainDefinition]:
    supabase_db = get_supabase_db()

    return supabase_db.update_api_brain_definition(brain_id, api_brain_definition)
