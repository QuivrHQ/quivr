from pathlib import Path
from uuid import uuid4

import pytest
from quivr_core.files.file import FileExtension, QuivrFile
from quivr_core.processor.implementations.default import ODTProcessor

unstructured = pytest.importorskip("unstructured")


@pytest.mark.unstructured
@pytest.mark.asyncio
async def test_odt_processor():
    p = Path("./tests/processor/odt/sample.odt")
    f = QuivrFile(
        id=uuid4(),
        brain_id=uuid4(),
        original_filename=p.stem,
        path=p,
        file_extension=FileExtension.odt,
        file_sha1="123",
    )
    processor = ODTProcessor()
    result = await processor.process_file(f)
    assert len(result) > 0


@pytest.mark.unstructured
@pytest.mark.asyncio
async def test_odt_processor_fail():
    p = Path("./tests/processor/odt/bad_odt.odt")
    f = QuivrFile(
        id=uuid4(),
        brain_id=uuid4(),
        original_filename=p.stem,
        path=p,
        file_extension=FileExtension.txt,
        file_sha1="123",
    )
    processor = ODTProcessor()
    with pytest.raises(ValueError):
        await processor.process_file(f)
