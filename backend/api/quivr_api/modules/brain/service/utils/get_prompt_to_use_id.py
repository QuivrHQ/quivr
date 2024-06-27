from typing import Optional
from uuid import UUID

from quivr_api.modules.brain.service.brain_service import BrainService

brain_service = BrainService()


def get_prompt_to_use_id(
    brain_id: Optional[UUID], prompt_id: Optional[UUID]
) -> Optional[UUID]:
    if brain_id is None and prompt_id is None:
        return None

    return (
        prompt_id
        if prompt_id
        else brain_service.get_brain_prompt_id(brain_id) if brain_id else None
    )
