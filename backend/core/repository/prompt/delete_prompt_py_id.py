from uuid import UUID

from fastapi import HTTPException
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

    response = (
        commons["supabase"]
        .from_("prompts")
        .delete()
        .filter("id", "eq", prompt_id)
        .execute()
    ).data
    if response == []:
        raise HTTPException(404, "Prompt not found")

    return Prompt(**response[0])
