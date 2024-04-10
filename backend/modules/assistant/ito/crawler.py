from bs4 import BeautifulSoup as Soup
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from logger import get_logger
from modules.assistant.ito.ito import ITO

logger = get_logger(__name__)


class CrawlerAssistant(ITO):

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            **kwargs,
        )

    async def process_assistant(self):

        url = self.url
        loader = RecursiveUrlLoader(
            url=url, max_depth=2, extractor=lambda x: Soup(x, "html.parser").text
        )
        docs = loader.load()

        nice_url = url.split("://")[1].replace("/", "_").replace(".", "_")
        nice_url += ".txt"

        for docs in docs:
            await self.create_and_upload_processed_file(
                docs.page_content, nice_url, "Crawler"
            )
