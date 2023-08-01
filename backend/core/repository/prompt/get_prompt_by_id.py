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

    response = (
        commons["supabase"]
        .from_("prompts")
        .select("*")
        .filter("id", "eq", prompt_id)
        .execute()
    ).data

    if response == []:
        return None
    return Prompt(**response[0])
