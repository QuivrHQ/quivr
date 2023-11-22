from uuid import UUID

from fastapi import HTTPException
from models.brain_entity import BrainType
from models.settings import get_supabase_db

from repository.api_brain_definition.delete_api_brain_definition import (
    delete_api_brain_definition,
)
from repository.brain import get_brain_by_id
from repository.brain.delete_brain_secrets import delete_brain_secrets_values
from repository.knowledge.remove_brain_all_knowledge import (
    remove_brain_all_knowledge,
)


def delete_brain(brain_id: UUID) -> dict[str, str]:
    supabase_db = get_supabase_db()

    brain_to_delete = get_brain_by_id(brain_id=brain_id)
    if brain_to_delete is None:
        raise HTTPException(status_code=404, detail="Brain not found.")

    if brain_to_delete.brain_type == BrainType.API:
        delete_brain_secrets_values(
            brain_id=brain_id,
        )
        delete_api_brain_definition(brain_id=brain_id)
    else:
        remove_brain_all_knowledge(brain_id)

    supabase_db.delete_brain_vector(str(brain_id))
    supabase_db.delete_brain_users(str(brain_id))
    supabase_db.delete_brain(str(brain_id))

    return {"message": "Brain deleted."}
