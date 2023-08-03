from uuid import UUID

from models.prompt import Prompt
from models.settings import common_dependencies


def get_prompt_by_id(prompt_id: UUID) -> Prompt | None:
    """
    Get a prompt by its id

    Args:
        prompt_id (UUID): The id of the prompt

    Returns:
        Prompt: The prompt
    """
    commons = common_dependencies()
    return commons["db"].get_prompt_by_id(prompt_id)
