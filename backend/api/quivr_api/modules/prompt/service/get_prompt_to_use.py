from typing import Optional
from uuid import UUID

from quivr_api.modules.brain.service.utils.get_prompt_to_use_id import (
    get_prompt_to_use_id,
)
from quivr_api.modules.prompt.service import PromptService

promptService = PromptService()


def get_prompt_to_use(brain_id: Optional[UUID], prompt_id: Optional[UUID]) -> str:
    prompt_to_use_id = get_prompt_to_use_id(brain_id, prompt_id)
    if prompt_to_use_id is None:
        return None

    return promptService.get_prompt_by_id(prompt_to_use_id)
