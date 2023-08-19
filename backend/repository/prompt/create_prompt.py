from models.databases.supabase.prompts import CreatePromptProperties
from models.prompt import Prompt
from models.settings import get_supabase_db


def create_prompt(prompt: CreatePromptProperties) -> Prompt:
    supabase_db = get_supabase_db()

    return supabase_db.create_prompt(prompt)
