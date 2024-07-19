from abc import ABC, abstractmethod

from langchain_core.documents import Document

from quivr_core.storage.file import FileExtension, QuivrFile


# TODO: processors should be cached somewhere ?
# The processor should be cached by processor type
# The cache should use a single
class ProcessorBase(ABC):
    supported_extensions: list[FileExtension | str]

    @abstractmethod
    async def process_file(self, file: QuivrFile) -> list[Document]:
        raise NotImplementedError

    def check_supported(self, file: QuivrFile):
        if file.file_extension not in self.supported_extensions:
            raise ValueError(f"can't process a file of type {file.file_extension}")
