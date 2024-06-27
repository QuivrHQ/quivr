from bs4 import BeautifulSoup as Soup
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from quivr_api.logger import get_logger
from quivr_api.modules.assistant.dto.outputs import (
    AssistantOutput,
    Inputs,
    InputUrl,
    OutputBrain,
    OutputEmail,
    Outputs,
)
from quivr_api.modules.assistant.ito.ito import ITO

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


def crawler_inputs():
    output = AssistantOutput(
        name="Crawler",
        description="Crawls a website and extracts the text from the pages",
        tags=["new"],
        input_description="One URL to crawl",
        output_description="Text extracted from the pages",
        inputs=Inputs(
            urls=[
                InputUrl(
                    key="url",
                    required=True,
                    description="The URL to crawl",
                )
            ],
        ),
        outputs=Outputs(
            brain=OutputBrain(
                required=True,
                description="The brain to which upload the document",
                type="uuid",
            ),
            email=OutputEmail(
                required=True,
                description="Send the document by email",
                type="str",
            ),
        ),
    )
    return output
