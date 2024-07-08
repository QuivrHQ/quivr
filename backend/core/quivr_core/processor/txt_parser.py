from langchain_community.document_loaders.text import TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter, TextSplitter

from quivr_core.processor.processor_base import ProcessorBase
from quivr_core.processor.splitter import SplitterConfig
from quivr_core.storage.file import QuivrFile


class TxtProcessor(ProcessorBase):
    def __init__(
        self,
        splitter: TextSplitter | None = None,
        splitter_config: SplitterConfig = SplitterConfig(),
    ) -> None:
        self.supported_extensions = [".txt"]
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
        if file.file_extension not in self.supported_extensions:
            raise Exception(f"can't process a file of type {file.file_extension}")

        loader = self.loader_cls(file.path)
        documents = await loader.aload()
        docs = self.text_splitter.split_documents(documents)
        return docs
