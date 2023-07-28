from typing import Union
from uuid import UUID

from logger import get_logger
from models.knowledge import Knowledge
from models.settings import common_dependencies

logger = get_logger(__name__)


def add_brain_knowledge(brain_id: UUID, knowledge_id: UUID):
    commons = common_dependencies()

    response = (
        commons["supabase"]
        .table("brain_knowledge")
        .insert({"brain_id": str(brain_id), "knowledge_id": str(knowledge_id)})
        .execute()
    )

    logger.info(f"Knowledge {knowledge_id} added to brain {brain_id} successfully")
    return response.data[0]
