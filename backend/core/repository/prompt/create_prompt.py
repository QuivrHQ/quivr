from models.databases.supabase.prompts import CreatePromptProperties
from models.prompt import Prompt
from models.settings import common_dependencies


def create_prompt(prompt: CreatePromptProperties) -> Prompt:
    """Create a prompt by id"""
    commons = common_dependencies()

    return commons["db"].create_prompt(prompt)
