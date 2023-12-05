from typing import Optional
from uuid import UUID

from llm.utils.get_prompt_to_use_id import get_prompt_to_use_id
from models.prompt import Prompt
from repository.prompt import get_prompt_by_id


def get_prompt_to_use(
    brain_id: Optional[UUID], prompt_id: Optional[UUID]
) -> Optional[Prompt]:
    prompt_to_use_id = get_prompt_to_use_id(brain_id, prompt_id)
    if prompt_to_use_id is None:
        return None

    return get_prompt_by_id(prompt_to_use_id)
