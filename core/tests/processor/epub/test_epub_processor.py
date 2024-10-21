from pathlib import Path
from uuid import uuid4

import pytest
from quivr_core.files.file import FileExtension, QuivrFile
from quivr_core.processor.implementations.default import EpubProcessor

unstructured = pytest.importorskip("unstructured")


@pytest.mark.unstructured
@pytest.mark.asyncio
async def test_epub_page_blanche():
    p = Path("./tests/processor/epub/page-blanche.epub")
    f = QuivrFile(
        id=uuid4(),
        brain_id=uuid4(),
        original_filename=p.stem,
        path=p,
        file_extension=FileExtension.epub,
        file_sha1="123",
    )
    processor = EpubProcessor()
    result = await processor.process_file(f)
    assert len(result) == 0


@pytest.mark.unstructured
@pytest.mark.asyncio
async def test_epub_processor():
    p = Path("./tests/processor/epub/sway.epub")
    f = QuivrFile(
        id=uuid4(),
        brain_id=uuid4(),
        original_filename=p.stem,
        path=p,
        file_extension=FileExtension.epub,
        file_sha1="123",
    )

    processor = EpubProcessor()
    result = await processor.process_file(f)
    assert len(result) > 0


@pytest.mark.unstructured
@pytest.mark.asyncio
async def test_epub_processor_fail(quivr_txt):
    processor = EpubProcessor()
    with pytest.raises(ValueError):
        await processor.process_file(quivr_txt)
