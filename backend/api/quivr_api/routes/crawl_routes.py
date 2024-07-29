from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request
from quivr_api.celery_worker import process_crawl_and_notify
from quivr_api.logger import get_logger
from quivr_api.middlewares.auth import AuthBearer, get_current_user
from quivr_api.modules.brain.entity.brain_entity import RoleEnum
from quivr_api.modules.brain.service.brain_authorization_service import (
    validate_brain_authorization,
)
from quivr_api.modules.knowledge.dto.inputs import CreateKnowledgeProperties
from quivr_api.modules.knowledge.service.knowledge_service import KnowledgeService
from quivr_api.modules.notification.dto.inputs import CreateNotification
from quivr_api.modules.notification.entity.notification import NotificationsStatusEnum
from quivr_api.modules.notification.service.notification_service import (
    NotificationService,
)
from quivr_api.modules.user.entity.user_identity import UserIdentity
from quivr_api.modules.user.service.user_usage import UserUsage
from quivr_api.packages.files.crawl.crawler import CrawlWebsite
from quivr_api.packages.files.file import convert_bytes

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
    bulk_id: Optional[UUID] = Query(None, description="The ID of the bulk upload"),
    brain_id: UUID = Query(..., description="The ID of the brain"),
    chat_id: Optional[UUID] = Query(None, description="The ID of the chat"),
    current_user: UserIdentity = Depends(get_current_user),
):
    """
    Crawl a website and process the crawled data.
    """

    validate_brain_authorization(
        brain_id, current_user.id, [RoleEnum.Editor, RoleEnum.Owner]
    )

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
        upload_notification = notification_service.add_notification(
            CreateNotification(
                user_id=current_user.id,
                bulk_id=bulk_id,
                status=NotificationsStatusEnum.INFO,
                title=f"{crawl_website.url}",
                category="crawl",
                brain_id=str(brain_id),
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
            knowledge_id=added_knowledge.id,
            notification_id=upload_notification.id,
        )

        return {"message": "Crawl processing has started."}
    return message
