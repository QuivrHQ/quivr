from uuid import UUID

from repository.brain.get_brain_by_id import get_brain_by_id


def get_brain_prompt_id(brain_id: UUID) -> UUID | None:
    brain = get_brain_by_id(brain_id)
    prompt_id = brain.brain_id if brain else None

    return prompt_id
