from importlib.metadata import version
from uuid import uuid4

from langchain_community.document_loaders.text import TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter, TextSplitter

from quivr_core.processor.processor_base import ProcessorBase
from quivr_core.processor.registry import FileExtension
from quivr_core.processor.splitter import SplitterConfig
from quivr_core.storage.file import QuivrFile


class TikTokenTxtProcessor(ProcessorBase):
    supported_extensions = [FileExtension.txt]

    def __init__(
        self,
        splitter: TextSplitter | None = None,
        splitter_config: SplitterConfig = SplitterConfig(),
    ) -> None:
        self.loader_cls = TextLoader

        self.splitter_config = splitter_config

        if splitter:
            self.text_splitter = splitter
        else:
            self.text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=splitter_config.chunk_size,
                chunk_overlap=splitter_config.chunk_overlap,
            )

    async def process_file(self, file: QuivrFile) -> list[Document]:
        self.check_supported(file)

        loader = self.loader_cls(file.path)
        documents = await loader.aload()
        docs = self.text_splitter.split_documents(documents)

        file_metadata = file.metadata

        for doc in docs:
            doc.metadata = {
                "id": uuid4(),
                "chunk_size": len(doc.page_content),
                "chunk_overlap": self.splitter_config.chunk_overlap,
                "parser_name": self.__class__.__name__,
                "quivr_core_version": version("quivr-core"),
                **file_metadata,
            }

        return docs
