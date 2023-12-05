from typing import Optional
from uuid import UUID

from celery_worker import process_crawl_and_notify
from fastapi import APIRouter, Depends, Query, Request
from logger import get_logger
from middlewares.auth import AuthBearer, get_current_user
from models import UserUsage
from modules.knowledge.dto.inputs import CreateKnowledgeProperties
from modules.knowledge.service.knowledge_service import KnowledgeService
from modules.notification.dto.inputs import CreateNotificationProperties
from modules.notification.entity.notification import NotificationsStatusEnum
from modules.notification.service.notification_service import NotificationService
from modules.user.entity.user_identity import UserIdentity
from packages.files.crawl.crawler import CrawlWebsite
from packages.files.file import convert_bytes

logger = get_logger(__name__)
crawl_router = APIRouter()

notification_service = NotificationService()
knowledge_service = KnowledgeService()


@crawl_router.get("/crawl/healthz", tags=["Health"])
async def healthz():
    return {"status": "ok"}


@crawl_router.post("/crawl", dependencies=[Depends(AuthBearer())], tags=["Crawl"])
async def crawl_endpoint(
    request: Request,
    crawl_website: CrawlWebsite,
    brain_id: UUID = Query(..., description="The ID of the brain"),
    chat_id: Optional[UUID] = Query(None, description="The ID of the chat"),
    current_user: UserIdentity = Depends(get_current_user),
):
    """
    Crawl a website and process the crawled data.
    """

    # [TODO] check if the user is the owner/editor of the brain

    userDailyUsage = UserUsage(
        id=current_user.id,
        email=current_user.email,
    )
    userSettings = userDailyUsage.get_user_settings()

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
            crawl_notification = notification_service.add_notification(
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

        added_knowledge = knowledge_service.add_knowledge(knowledge_to_add)
        logger.info(f"Knowledge {added_knowledge} added successfully")

        process_crawl_and_notify.delay(
            crawl_website_url=crawl_website.url,
            brain_id=brain_id,
            notification_id=crawl_notification.id,
        )

        return {"message": "Crawl processing has started."}
    return message
