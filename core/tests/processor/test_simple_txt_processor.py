import pytest
from langchain_core.documents import Document
from quivr_core.files.file import FileExtension
from quivr_core.processor.implementations.simple_txt_processor import (
    SimpleTxtProcessor,
    recursive_character_splitter,
)
from quivr_core.processor.splitter import SplitterConfig


def test_recursive_character_splitter():
    doc = Document(page_content="abcdefgh", metadata={"key": "value"})

    docs = recursive_character_splitter(doc, chunk_size=2, chunk_overlap=1)

    assert [d.page_content for d in docs] == ["ab", "bc", "cd", "de", "ef", "fg", "gh"]
    assert [d.metadata for d in docs] == [doc.metadata] * len(docs)


@pytest.mark.asyncio
async def test_simple_processor(quivr_pdf, quivr_txt):
    proc = SimpleTxtProcessor(
        splitter_config=SplitterConfig(chunk_size=100, chunk_overlap=20)
    )
    assert proc.supported_extensions == [FileExtension.txt]

    with pytest.raises(ValueError):
        await proc.process_file(quivr_pdf)

    docs = await proc.process_file(quivr_txt)

    assert len(docs) == 1
    assert docs[0].page_content == "This is some test data."
