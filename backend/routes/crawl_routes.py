import os
import shutil
from tempfile import SpooledTemporaryFile
from uuid import UUID

from auth import AuthBearer, get_current_user
from crawl.crawler import CrawlWebsite
from fastapi import APIRouter, Depends, Query, Request, UploadFile
from models.brains import Brain
from models.files import File
from models.settings import common_dependencies
from models.users import User
from parsers.github import process_github
from utils.file import convert_bytes
from utils.processors import filter_file

crawl_router = APIRouter()


@crawl_router.post("/crawl", dependencies=[Depends(AuthBearer())], tags=["Crawl"])
async def crawl_endpoint(
    request: Request,
    crawl_website: CrawlWebsite,
    brain_id: UUID = Query(..., description="The ID of the brain"),
    enable_summarization: bool = False,
    current_user: User = Depends(get_current_user),
):
    """
    Crawl a website and process the crawled data.
    """

    # [TODO] check if the user is the owner/editor of the brain
    brain = Brain(id=brain_id)

    commons = common_dependencies()

    if request.headers.get("Openai-Api-Key"):
        brain.max_brain_size = os.getenv(
            "MAX_BRAIN_SIZE_WITH_KEY", 209715200
        )  # pyright: ignore reportPrivateUsage=none

    file_size = 1000000
    remaining_free_space = brain.remaining_brain_size

    if remaining_free_space - file_size < 0:
        message = {
            "message": f"❌ User's brain will exceed maximum capacity with this upload. Maximum file allowed is : {convert_bytes(remaining_free_space)}",
            "type": "error",
        }
    else:
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
                commons,
                file,
                enable_summarization,
                brain.id,
                openai_api_key=request.headers.get("Openai-Api-Key", None),
            )
            return message
        else:
            #  check remaining free space here !!
            message = await process_github(
                commons,
                crawl_website.url,
                "false",
                brain_id,
                user_openai_api_key=request.headers.get("Openai-Api-Key", None),
            )
