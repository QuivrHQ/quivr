from uuid import UUID

from models.prompt import Prompt
from models.settings import common_dependencies


def delete_prompt_by_id(prompt_id: UUID) -> Prompt | None:
    """
    Delete a prompt by id
    Args:
        prompt_id (UUID): The id of the prompt

    Returns:
        Prompt: The prompt
    """
    commons = common_dependencies()
    return commons["db"].delete_prompt_by_id(prompt_id)
