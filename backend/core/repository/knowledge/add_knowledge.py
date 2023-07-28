from logger import get_logger
from models.knowledge import Knowledge
from models.settings import common_dependencies

logger = get_logger(__name__)


def add_knowledge(knowledge: Knowledge):
    commons = common_dependencies()

    response = (
        commons["supabase"]
        .table("knowledge")
        .insert(
            {
                "file_id": str(knowledge.file_id),
                "url": knowledge.url,
                "content_sha1": knowledge.content_sha1,
                "user_id": str(knowledge.owner_id),
                # TODO: Handle invalid characters in name -> different langugages etc
                # storage3.utils.StorageException: {'statusCode': 400, 'error': 'Invalid Input', 'message': 'The object name contains invalid characters'}
                "knowledge_name": knowledge.name,
                "summary": knowledge.summary,
                "extension": knowledge.extension,
            }
        )
        .execute()
    )

    logger.info(f"response {response} ")
    # try:
    #     logger.info(response.data)
    # except Exception as e:
    #     logger.info("no data1", e)
    # try:
    #     logger.info(response.data)
    # except Exception as e:
    #     logger.info("no data2", e)

    knowledge_id = response.data[0]["id"]

    logger.info(f"Knowledge {knowledge_id} added successfully")
    return response.data[0]
