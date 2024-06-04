import os
import re
import tempfile
import unicodedata

from langchain_community.document_loaders import PlaywrightURLLoader
from logger import get_logger
from pydantic import BaseModel

logger = get_logger(__name__)


class CrawlWebsite(BaseModel):
    url: str
    js: bool = False
    depth: int = int(os.getenv("CRAWL_DEPTH", "1"))
    max_pages: int = 100
    max_time: int = 60

    def process(self):
        # Extract and combine content recursively
        loader = PlaywrightURLLoader(
            urls=[self.url], remove_selectors=["header", "footer"]
        )
        data = loader.load()

        # Now turn the data into a string
        logger.info(f"Extracted content from {len(data)} pages")
        logger.info(data)
        extracted_content = ""
        for page in data:
            extracted_content += page.page_content

        # Create a file
        file_name = slugify(self.url) + ".txt"
        temp_file_path = os.path.join(tempfile.gettempdir(), file_name)
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(extracted_content)  # type: ignore

        return temp_file_path, file_name

    def checkGithub(self):
        return "github.com" in self.url


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    text = re.sub(r"[-\s]+", "-", text)
    return text
