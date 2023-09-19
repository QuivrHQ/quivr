from logger import get_logger
from models.databases.supabase.knowledge import CreateKnowledgeProperties
from models.knowledge import Knowledge
from models.settings import get_supabase_db

logger = get_logger(__name__)


def add_knowledge(knowledge: Knowledge):
    supabase_db = get_supabase_db()

    knowledge_to_add = CreateKnowledgeProperties(**knowledge.dict())
    knowledge = supabase_db.insert_knowledge(knowledge_to_add)

    logger.info(f"Knowledge { knowledge.id} added successfully")
    return knowledge
