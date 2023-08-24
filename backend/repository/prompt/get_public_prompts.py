from models import Prompt, get_supabase_db
from typing import List


def get_public_prompts() -> List[Prompt]:
    """
    List all public prompts
    """
    supabase_db = get_supabase_db()
    return supabase_db.get_public_prompts()
