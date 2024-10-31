import logging
import os

import httpx
import tiktoken
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter, TextSplitter
from quivr_core.config import MegaparseConfig
from quivr_core.files.file import QuivrFile
from quivr_core.processor.processor_base import ProcessorBase
from quivr_core.processor.registry import FileExtension
from quivr_core.processor.splitter import SplitterConfig

logger = logging.getLogger("quivr_core")


class MegaparseProcessor(ProcessorBase):
    """
    Megaparse processor for PDF files.

    It can be used to parse PDF files and split them into chunks.

    It comes from the megaparse library.

    ## Installation
    ```bash
    pip install megaparse
    ```

    """

    supported_extensions = [
        FileExtension.pdf,
        FileExtension.docx,
        FileExtension.doc,
        FileExtension.pptx,
        FileExtension.xls,
        FileExtension.xlsx,
        FileExtension.csv,
        FileExtension.epub,
        FileExtension.bib,
        FileExtension.odt,
        FileExtension.html,
        FileExtension.py,
        FileExtension.markdown,
        FileExtension.md,
        FileExtension.mdx,
        FileExtension.ipynb,
    ]

    def __init__(
        self,
        splitter: TextSplitter | None = None,
        splitter_config: SplitterConfig = SplitterConfig(),
        megaparse_config: MegaparseConfig = MegaparseConfig(),
    ) -> None:
        self.enc = tiktoken.get_encoding("cl100k_base")
        self.splitter_config = splitter_config
        self.megaparse_config = megaparse_config

        if splitter:
            self.text_splitter = splitter
        else:
            self.text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=splitter_config.chunk_size,
                chunk_overlap=splitter_config.chunk_overlap,
            )

    @property
    def processor_metadata(self):
        return {
            "chunk_overlap": self.splitter_config.chunk_overlap,
        }

    async def process_file_inner(self, file: QuivrFile) -> list[Document]:
        megaparse_url = os.getenv("MEGAPARSE_URL_API", "http://localhost:8000")
        megaparse_api_key = os.getenv("MEGAPARSE_API_KEY", "megaparse_api_key")
        with open(file.path, "rb") as f:
            files = {"file": (os.path.basename(file.path), f)}
            data = {
                "method": self.megaparse_config.method,
                "strategy": self.megaparse_config.strategy,
                "check_table": self.megaparse_config.check_table,
                "parsing_instruction": self.megaparse_config.parsing_instruction,
                "model_name": self.megaparse_config.model_name,
            }
            headers = {"Authorization": f"Bearer {megaparse_api_key}"}
            async with httpx.AsyncClient(
                timeout=self.megaparse_config.timeout
            ) as client:
                response = await client.post(
                    f"{megaparse_url}/file", files=files, data=data, headers=headers
                )

        if response.status_code == 200:
            result = response.json().get("result")
            document = Document(page_content=result)
            if len(document.page_content) > 0:
                docs = self.text_splitter.split_documents([document])
                for doc in docs:
                    doc.metadata = {
                        "chunk_size": len(self.enc.encode(doc.page_content))
                    }
                return docs
            raise Exception("Failed to parse file, we were returned an empty result")
        else:
            logger.error(f"Failed to process file: {response.text}")
            return []
