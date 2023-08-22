from typing import Optional
from uuid import UUID

from repository.brain import get_brain_prompt_id


def get_prompt_to_use_id(
    brain_id: Optional[UUID], prompt_id: Optional[UUID]
) -> Optional[UUID]:
    if brain_id is None and prompt_id is None:
        return None

    return (
        prompt_id if prompt_id else get_brain_prompt_id(brain_id) if brain_id else None
    )
