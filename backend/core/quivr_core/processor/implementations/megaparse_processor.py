import logging

import tiktoken
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter, TextSplitter
from quivr_core.processor.megaparse import MegaParse
from quivr_core.processor.megaparse.config import MegaparseConfig

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

    supported_extensions = [FileExtension.pdf]

    def __init__(
        self,
        splitter: TextSplitter | None = None,
        splitter_config: SplitterConfig = SplitterConfig(),
        megaparse_config: MegaparseConfig = MegaparseConfig(),
    ) -> None:
        self.loader_cls = MegaParse
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
        mega_parse = MegaParse(file_path=file.path, config=self.megaparse_config)  # type: ignore
        document: Document = await mega_parse.aload()
        if len(document.page_content) > self.splitter_config.chunk_size:
            docs = self.text_splitter.split_documents([document])
            for doc in docs:
                # if "Production Fonts (maximum)" in doc.page_content:
                #    print('Doc: ', doc.page_content)
                doc.metadata = {"chunk_size": len(self.enc.encode(doc.page_content))}
            return docs
        return [document]
