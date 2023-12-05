from uuid import UUID

from models.databases.supabase.prompts import PromptUpdatableProperties
from models import Prompt, get_supabase_db


def update_prompt_by_id(prompt_id: UUID, prompt: PromptUpdatableProperties) -> Prompt:
    """Update a prompt by id"""
    supabase_db = get_supabase_db()

    return supabase_db.update_prompt_by_id(prompt_id, prompt)
