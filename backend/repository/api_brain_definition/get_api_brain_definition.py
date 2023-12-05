from typing import Optional
from uuid import UUID

from models import get_supabase_db
from modules.brain.entity.api_brain_definition_entity import ApiBrainDefinition


def get_api_brain_definition(brain_id: UUID) -> Optional[ApiBrainDefinition]:
    supabase_db = get_supabase_db()

    return supabase_db.get_api_brain_definition(brain_id)
