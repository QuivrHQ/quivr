from abc import ABC, abstractmethod

from langchain_core.documents import Document

from quivr_core.storage.file import FileExtension, QuivrFile


class ProcessorBase(ABC):
    supported_extensions: list[FileExtension]

    @abstractmethod
    async def process_file(self, file: QuivrFile) -> list[Document]:
        raise NotImplementedError

    def check_supported(self, file: QuivrFile):
        if file.file_extension not in self.supported_extensions:
            raise ValueError(f"can't process a file of type {file.file_extension}")
