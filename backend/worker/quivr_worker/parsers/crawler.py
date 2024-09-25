import os
import re
import unicodedata

from langchain_community.document_loaders import PlaywrightURLLoader
from pydantic import BaseModel
from quivr_api.logger import get_logger

logger = get_logger("celery_worker")


class URL(BaseModel):
    url: str
    js: bool = False
    depth: int = int(os.getenv("CRAWL_DEPTH", "1"))
    max_pages: int = 100
    max_time: int = 60


async def extract_from_url(url: URL) -> str:
    # Extract and combine content recursively
    loader = PlaywrightURLLoader(urls=[url.url], remove_selectors=["header", "footer"])

    data = await loader.aload()
    # Now turn the data into a string
    logger.info(f"Extracted content from {len(data)} pages")
    extracted_content = ""
    for page in data:
        extracted_content += page.page_content
    return extracted_content


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    text = re.sub(r"[-\s]+", "-", text)
    return text
