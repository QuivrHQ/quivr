import logging

import tiktoken
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter, TextSplitter
from megaparse.Converter import MegaParse

from quivr_core.files.file import QuivrFile
from quivr_core.processor.processor_base import ProcessorBase
from quivr_core.processor.registry import FileExtension
from quivr_core.processor.splitter import SplitterConfig

logger = logging.getLogger("quivr_core")


class MegaparseProcessor(ProcessorBase):
    supported_extensions = [FileExtension.pdf]

    def __init__(
        self,
        splitter: TextSplitter | None = None,
        splitter_config: SplitterConfig = SplitterConfig(),
    ) -> None:
        self.loader_cls = MegaParse(file_path="./test.pdf")
        self.enc = tiktoken.get_encoding("cl100k_base")
        self.splitter_config = splitter_config

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
        loader = self.loader_cls(file_path=file.path, **self.loader_kwargs)  # type: ignore
        documents = await loader.aload()
        docs = self.text_splitter.split_documents(documents)

        for doc in docs:
            doc.metadata = {"chunk_size": len(self.enc.encode(doc.page_content))}
        return docs
