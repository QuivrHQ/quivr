from logger import get_logger
from models.knowledge import Knowledge

from backend.models.databases.supabase.knowledge import CreateKnowledgeProperties
from backend.models.settings import get_supabase_db

logger = get_logger(__name__)


def add_knowledge(knowledge: Knowledge):
    supabase_db = get_supabase_db()

    knowledge_to_add = CreateKnowledgeProperties(
        file_id=knowledge.file_id,
        url=knowledge.url,
        content_sha1=knowledge.content_sha1,
        owner_id=knowledge.owner_id,
        # TODO: Handle invalid characters in name -> different langugages etc
        # storage3.utils.StorageException: {'statusCode': 400, 'error': 'Invalid Input', 'message': 'The object name contains invalid characters'}
        name=knowledge.name,
        summary=knowledge.summary,
        extension=knowledge.extension,
    )
    knowledge = supabase_db.insert_knowledge(knowledge_to_add)

    logger.info(f"response {knowledge} ")
    # try:
    #     logger.info(response.data)
    # except Exception as e:
    #     logger.info("no data1", e)
    # try:
    #     logger.info(response.data)
    # except Exception as e:
    #     logger.info("no data2", e)

    logger.info(f"Knowledge { knowledge.id} added successfully")
    return knowledge
