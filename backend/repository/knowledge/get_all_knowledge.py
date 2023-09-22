from uuid import UUID

from logger import get_logger
from models.settings import get_supabase_db

logger = get_logger(__name__)


def get_all_knowledge(brain_id: UUID):
    supabase_db = get_supabase_db()

    knowledges = supabase_db.get_all_knowledge_in_brain(brain_id)

    return knowledges
