from uuid import UUID

from logger import get_logger

from backend.models.databases.supabase.brain_knowledge import (
    CreateBrainKnowledgeProperties,
)
from backend.models.settings import get_supabase_db

logger = get_logger(__name__)


def add_brain_knowledge(brain_id: UUID, knowledge_id: UUID):
    supabase_db = get_supabase_db()

    new_brain_knowledge = CreateBrainKnowledgeProperties(
        brain_id=brain_id, knowledge_id=knowledge_id
    )

    brain_knowledge = supabase_db.insert_brain_knowledge(new_brain_knowledge)

    logger.info(f"Knowledge {knowledge_id} added to brain {brain_id} successfully")
    return brain_knowledge
