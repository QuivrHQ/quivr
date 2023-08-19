from models.prompt import Prompt
from models.settings import get_supabase_db


def get_public_prompts() -> list[Prompt]:
    """
    List all public prompts
    """
    supabase_db = get_supabase_db()
    return supabase_db.get_public_prompts()
