from abc import ABC, abstractmethod
from importlib.metadata import PackageNotFoundError, version
from typing import Any
from uuid import uuid4

from langchain_core.documents import Document

from quivr_core.files.file import FileExtension, QuivrFile


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
        try:
            qvr_version = version("quivr-core")
        except PackageNotFoundError:
            qvr_version = "dev"

        for idx, doc in enumerate(docs):
            doc.metadata = {
                "id": uuid4(),
                "chunk_index": idx,
                "quivr_core_version": qvr_version,
                **file.metadata,
                **doc.metadata,
                **self.processor_metadata,
            }
        return docs

    @abstractmethod
    async def process_file_inner(self, file: QuivrFile) -> list[Document]:
        raise NotImplementedError
