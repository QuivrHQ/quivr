from uuid import UUID

from logger import get_logger
from models.settings import get_supabase_db

logger = get_logger(__name__)


def remove_knowledge(knowledge_id: UUID):
    supabase_db = get_supabase_db()

    message = supabase_db.remove_knowledge_by_id(knowledge_id)

    logger.info(f"Knowledge { knowledge_id} removed successfully from table")

    return message
