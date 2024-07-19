from abc import ABC, abstractmethod
from importlib.metadata import version
from typing import Any
from uuid import uuid4

import tiktoken
from langchain_core.documents import Document

from quivr_core.storage.file import FileExtension, QuivrFile

enc = tiktoken.get_encoding("cl100k_base")


# TODO: processors should be cached somewhere ?
# The processor should be cached by processor type
# The cache should use a single
class ProcessorBase(ABC):
    supported_extensions: list[FileExtension | str]

    def check_supported(self, file: QuivrFile):
        if file.file_extension not in self.supported_extensions:
            raise ValueError(f"can't process a file of type {file.file_extension}")

    @property
    @abstractmethod
    def processor_metadata(self) -> dict[str, Any]:
        raise NotImplementedError

    async def process_file(self, file: QuivrFile) -> list[Document]:
        self.check_supported(file)
        docs = await self.process_file_inner(file)
        for idx, doc in enumerate(docs):
            len_chunk = len(enc.encode(doc.page_content))
            doc.metadata = {
                "id": uuid4(),
                "chunk_index": idx,
                "chunk_size": len_chunk,
                "parser_name": self.__class__.__name__,
                "quivr_core_version": version("quivr-core"),
                **file.metadata,
                **doc.metadata,
                **self.processor_metadata,
            }
        return docs

    @abstractmethod
    async def process_file_inner(self, file: QuivrFile) -> list[Document]:
        raise NotImplementedError
