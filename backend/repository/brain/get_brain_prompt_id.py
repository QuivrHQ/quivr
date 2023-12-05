from uuid import UUID

from repository.brain import get_brain_by_id


def get_brain_prompt_id(brain_id: UUID) -> UUID | None:
    brain = get_brain_by_id(brain_id)
    prompt_id = brain.prompt_id if brain else None

    return prompt_id
