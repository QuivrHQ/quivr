import asyncio

from celery_config import celery
from langchain_core.documents import Document
from logger import get_logger

from .ito import OutputHandler
from .summary import map_reduce_chain

logger = get_logger(__name__)


@celery.task(name="task_summary")
def task_summary(
    split_docs, filename, brain_id, email_activated, current_user, notification_id
):
    loop = asyncio.get_event_loop()
    # turn split_docs into a list of Document objects
    logger.info("split_docs: %s", split_docs)
    split_docs = [
        Document(
            page_content=doc["kwargs"]["page_content"],
            metadata=doc["kwargs"]["metadata"],
        )
        for doc in split_docs
        if "kwargs" in doc
        and "page_content" in doc["kwargs"]
        and "metadata" in doc["kwargs"]
    ]
    content = map_reduce_chain().run(split_docs)
    output_handler = OutputHandler()
    return loop.run_until_complete(
        output_handler.create_and_upload_processed_file(
            content,
            filename,
            "Summary",
            content,
            "Summary",
            "Summary",
            brain_id,
            email_activated,
            current_user,
            notification_id,
        )
    )
