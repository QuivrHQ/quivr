from uuid import UUID

from logger import get_logger
from models.settings import get_supabase_db

logger = get_logger(__name__)


def remove_brain_all_knowledge(brain_id: UUID) -> None:
    supabase_db = get_supabase_db()

    supabase_db.remove_brain_all_knowledge(brain_id)

    logger.info(f"All knowledge in brain {brain_id} removed successfully from table")
