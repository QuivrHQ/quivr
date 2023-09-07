import os
import shutil
from tempfile import SpooledTemporaryFile
from uuid import UUID

from auth import AuthBearer, get_current_user
from crawl.crawler import CrawlWebsite
from fastapi import APIRouter, Depends, Query, Request, UploadFile
from models import Brain, File, UserIdentity
from models.databases.supabase.notifications import (
    CreateNotificationProperties,
    NotificationUpdatableProperties,
)
from models.notifications import NotificationsStatusEnum
from parsers.github import process_github
from repository.notification.add_notification import add_notification
from repository.notification.update_notification import (
    update_notification_by_id,
)
from utils.file import convert_bytes
from utils.processors import filter_file

crawl_router = APIRouter()


@crawl_router.get("/crawl/healthz", tags=["Health"])
async def healthz():
    return {"status": "ok"}


@crawl_router.post("/crawl", dependencies=[Depends(AuthBearer())], tags=["Crawl"])
async def crawl_endpoint(
    request: Request,
    crawl_website: CrawlWebsite,
    brain_id: UUID = Query(..., description="The ID of the brain"),
    enable_summarization: bool = False,
    current_user: UserIdentity = Depends(get_current_user),
):
    """
    Crawl a website and process the crawled data.
    """

    # [TODO] check if the user is the owner/editor of the brain
    brain = Brain(id=brain_id)

    # [TODO] rate limiting of user for crawl
    if request.headers.get("Openai-Api-Key"):
        brain.max_brain_size = int(os.getenv("MAX_BRAIN_SIZE_WITH_KEY", 209715200))

    file_size = 1000000
    remaining_free_space = brain.remaining_brain_size

    if remaining_free_space - file_size < 0:
        message = {
            "message": f"❌ UserIdentity's brain will exceed maximum capacity with this upload. Maximum file allowed is : {convert_bytes(remaining_free_space)}",
            "type": "error",
        }
    else:
        crawl_notification = add_notification(
            CreateNotificationProperties(
                action="CRAWL",
            )
        )
        if not crawl_website.checkGithub():
            (
                file_path,
                file_name,
            ) = crawl_website.process()  # pyright: ignore reportPrivateUsage=none
            # Create a SpooledTemporaryFile from the file_path
            spooled_file = SpooledTemporaryFile()
            with open(file_path, "rb") as f:
                shutil.copyfileobj(f, spooled_file)

            # Pass the SpooledTemporaryFile to UploadFile
            uploadFile = UploadFile(
                file=spooled_file,  # pyright: ignore reportPrivateUsage=none
                filename=file_name,
            )
            file = File(file=uploadFile)
            #  check remaining free space here !!
            message = await filter_file(
                file=file,
                enable_summarization=enable_summarization,
                brain_id=brain.id,
                openai_api_key=request.headers.get("Openai-Api-Key", None),
            )
        else:
            #  check remaining free space here !!
            message = await process_github(
                repo=crawl_website.url,
                enable_summarization="false",
                brain_id=brain_id,
                user_openai_api_key=request.headers.get("Openai-Api-Key", None),
            )
        update_notification_by_id(
            crawl_notification.id,
            NotificationUpdatableProperties(
                status=NotificationsStatusEnum.Done, message=str(message)
            ),
        )
    return message
