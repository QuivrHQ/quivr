from uuid import UUID

from models.databases.supabase.prompts import PromptUpdatableProperties
from models.prompt import Prompt
from models.settings import common_dependencies


def update_prompt_by_id(prompt_id: UUID, prompt: PromptUpdatableProperties) -> Prompt:
    """Update a prompt by id"""
    commons = common_dependencies()

    return commons["db"].update_prompt_by_id(prompt_id, prompt)
