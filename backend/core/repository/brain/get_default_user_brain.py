from uuid import UUID

from logger import get_logger
from models.brain_entity import BrainEntity
from models.settings import get_supabase_db
from repository.brain.get_brain_by_id import get_brain_by_id

logger = get_logger(__name__)


def get_user_default_brain(user_id: UUID) -> BrainEntity | None:
    supabase_db = get_supabase_db()
    brain_id = supabase_db.get_default_user_brain_id(user_id)

    logger.info("Default brain response:", brain_id)

    if brain_id is None:
        return None

    logger.info(f"Default brain id: {brain_id}")

    return get_brain_by_id(brain_id)
