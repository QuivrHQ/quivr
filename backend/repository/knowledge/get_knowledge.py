from uuid import UUID

from logger import get_logger
from models.knowledge import Knowledge
from models.settings import get_supabase_db

logger = get_logger(__name__)


def get_knowledge(knowledge_id: UUID) -> Knowledge:
    supabase_db = get_supabase_db()

    knowledge = supabase_db.get_knowledge_by_id(knowledge_id)

    return knowledge
