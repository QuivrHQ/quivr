from pathlib import Path
from uuid import uuid4

import pytest
from quivr_core.files.file import FileExtension, QuivrFile
from quivr_core.processor.implementations.default import MarkdownProcessor

unstructured = pytest.importorskip("unstructured")


@pytest.mark.unstructured
@pytest.mark.asyncio
async def test_markdown_processor():
    p = Path("./tests/processor/data/guidelines_code.md")
    f = QuivrFile(
        id=uuid4(),
        brain_id=uuid4(),
        original_filename=p.stem,
        path=p,
        file_extension=FileExtension.md,
        file_sha1="123",
    )
    processor = MarkdownProcessor()
    result = await processor.process_file(f)
    assert len(result) > 0


@pytest.mark.unstructured
@pytest.mark.asyncio
async def test_markdown_processor_fail(quivr_txt):
    processor = MarkdownProcessor()
    with pytest.raises(ValueError):
        await processor.process_file(quivr_txt)
