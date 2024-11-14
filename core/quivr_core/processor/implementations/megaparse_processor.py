import logging

import tiktoken
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter, TextSplitter
from megaparse.core.megaparse import MegaParse
from megaparse.core.parser.unstructured_parser import UnstructuredParser

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
        logger.info(f"Uploading file {file.path} to MegaParse")
        parser = UnstructuredParser(**self.megaparse_config.model_dump())
        megaparse = MegaParse(parser)
        response = await megaparse.aload(file.path)
        logger.info(f"File :  {response}")
        document = Document(
            page_content=response,
        )

        docs = self.text_splitter.split_documents([document])
        for doc in docs:
            doc.metadata = {"chunk_size": len(self.enc.encode(doc.page_content))}
        return docs

    # async def process_file_inner(self, file: QuivrFile) -> list[Document]:
    #     api_key = str(os.getenv("MEGAPARSE_API_KEY"))
    #     megaparse = MegaParseSDK(api_key)
    #     logger.info(f"Uploading file {file.path} to MegaParse")
    #     data = {
    #         "method": self.megaparse_config.method,
    #         "strategy": self.megaparse_config.strategy,
    #         "check_table": self.megaparse_config.check_table,
    #         "parsing_instruction": self.megaparse_config.parsing_instruction,
    #         "model_name": self.megaparse_config.model_name,
    #     }
    #     response = await megaparse.file.upload(
    #         file_path=str(file.path),
    #         **data,
    #     )
    #     document = Document(
    #         page_content=response["result"],
    #     )
    #     if len(response) > self.splitter_config.chunk_size:
    #         docs = self.text_splitter.split_documents([document])
    #         for doc in docs:
    #             doc.metadata = {"chunk_size": len(self.enc.encode(doc.page_content))}
    #         return docs
    #     return [document]
