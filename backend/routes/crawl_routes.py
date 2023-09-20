from typing import Optional
from uuid import UUID

from auth import AuthBearer, get_current_user
from celery_worker import process_crawl_and_notify
from crawl.crawler import CrawlWebsite
from fastapi import APIRouter, Depends, Query, Request
from logger import get_logger
from models import Brain, UserIdentity, UserUsage
from models.databases.supabase.knowledge import CreateKnowledgeProperties
from models.databases.supabase.notifications import CreateNotificationProperties
from models.notifications import NotificationsStatusEnum
from repository.knowledge.add_knowledge import add_knowledge
from repository.notification.add_notification import add_notification
from utils.file import convert_bytes

logger = get_logger(__name__)
crawl_router = APIRouter()


@crawl_router.get("/crawl/healthz", tags=["Health"])
async def healthz():
    return {"status": "ok"}


@crawl_router.post("/crawl", dependencies=[Depends(AuthBearer())], tags=["Crawl"])
async def crawl_endpoint(
    request: Request,
    crawl_website: CrawlWebsite,
    brain_id: UUID = Query(..., description="The ID of the brain"),
    chat_id: Optional[UUID] = Query(None, description="The ID of the chat"),
    enable_summarization: bool = False,
    current_user: UserIdentity = Depends(get_current_user),
):
    """
    Crawl a website and process the crawled data.
    """

    # [TODO] check if the user is the owner/editor of the brain
    brain = Brain(id=brain_id)

    userDailyUsage = UserUsage(
        id=current_user.id,
        email=current_user.email,
        openai_api_key=current_user.openai_api_key,
    )
    userSettings = userDailyUsage.get_user_settings()

    # [TODO] rate limiting of user for crawl
    if request.headers.get("Openai-Api-Key"):
        brain.max_brain_size = userSettings.get("max_brain_size", 1000000000)

    file_size = 1000000
    remaining_free_space = userSettings.get("max_brain_size", 1000000000)

    if remaining_free_space - file_size < 0:
        message = {
            "message": f"❌ UserIdentity's brain will exceed maximum capacity with this upload. Maximum file allowed is : {convert_bytes(remaining_free_space)}",
            "type": "error",
        }
    else:
        crawl_notification = None
        if chat_id:
            crawl_notification = add_notification(
                CreateNotificationProperties(
                    action="CRAWL",
                    chat_id=chat_id,
                    status=NotificationsStatusEnum.Pending,
                )
            )

        knowledge_to_add = CreateKnowledgeProperties(
            brain_id=brain_id,
            url=crawl_website.url,
            extension="html",
        )

        added_knowledge = add_knowledge(knowledge_to_add)
        logger.info(f"Knowledge {added_knowledge} added successfully")

        process_crawl_and_notify.delay(
            crawl_website_url=crawl_website.url,
            enable_summarization=enable_summarization,
            brain_id=brain_id,
            openai_api_key=request.headers.get("Openai-Api-Key", None),
            notification_id=crawl_notification.id,
        )

        return {"message": "Crawl processing has started."}
    return message
