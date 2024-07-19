from importlib.metadata import version
from uuid import uuid4

import aiofiles
from langchain_core.documents import Document

from quivr_core.processor.processor_base import ProcessorBase
from quivr_core.processor.registry import FileExtension
from quivr_core.processor.splitter import SplitterConfig
from quivr_core.storage.file import QuivrFile


def recursive_character_splitter(
    doc: Document, chunk_size: int, chunk_overlap: int
) -> list[Document]:
    assert chunk_overlap < chunk_size, "chunk_overlap is greater than chunk_size"

    if len(doc.page_content) <= chunk_size:
        return [doc]

    chunk = Document(page_content=doc.page_content[:chunk_size], metadata=doc.metadata)
    remaining = Document(
        page_content=doc.page_content[chunk_size - chunk_overlap :],
        metadata=doc.metadata,
    )

    return [chunk] + recursive_character_splitter(remaining, chunk_size, chunk_overlap)


class SimpleTxtProcessor(ProcessorBase):
    supported_extensions = [FileExtension.txt]

    def __init__(
        self, splitter_config: SplitterConfig = SplitterConfig(), **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.splitter_config = splitter_config

    async def process_file(self, file: QuivrFile) -> list[Document]:
        self.check_supported(file)
        file_metadata = file.metadata

        async with aiofiles.open(file.path, mode="r") as f:
            content = await f.read()

        doc = Document(
            page_content=content,
            metadata={
                "id": uuid4(),
                "chunk_size": len(content),
                "chunk_overlap": self.splitter_config.chunk_overlap,
                "parser_name": self.__class__.__name__,
                "quivr_core_version": version("quivr-core"),
                **file_metadata,
            },
        )

        docs = recursive_character_splitter(
            doc, self.splitter_config.chunk_size, self.splitter_config.chunk_overlap
        )

        return docs
