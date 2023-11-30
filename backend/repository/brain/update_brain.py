from uuid import UUID

from fastapi import HTTPException
from models import get_supabase_db
from modules.brain.entity.brain_entity import BrainEntity, BrainType
from modules.brain.repository.brains import BrainUpdatableProperties
from repository.api_brain_definition.update_api_brain_definition import (
    update_api_brain_definition,
)
from repository.brain.delete_brain_secrets import delete_brain_secrets_values


