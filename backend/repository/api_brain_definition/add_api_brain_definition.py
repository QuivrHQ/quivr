from uuid import UUID

from models.databases.supabase.api_brain_definition import (
    CreateApiBrainDefinition,
)
from models.settings import get_supabase_db


def add_api_brain_definition(
    brain_id: UUID, api_brain_definition: CreateApiBrainDefinition
) -> None:
    supabase_db = get_supabase_db()

    supabase_db.add_api_brain_definition(brain_id, api_brain_definition)
