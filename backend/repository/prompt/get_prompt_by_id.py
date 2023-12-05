from uuid import UUID

from models import Prompt, get_supabase_db


def get_prompt_by_id(prompt_id: UUID) -> Prompt | None:
    """
    Get a prompt by its id

    Args:
        prompt_id (UUID): The id of the prompt

    Returns:
        Prompt: The prompt
    """
    supabase_db = get_supabase_db()
    return supabase_db.get_prompt_by_id(prompt_id)
