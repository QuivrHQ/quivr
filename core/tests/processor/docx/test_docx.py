from pathlib import Path
from uuid import uuid4

import pytest
from quivr_core.files.file import FileExtension, QuivrFile
from quivr_core.processor.implementations.default import DOCXProcessor

unstructured = pytest.importorskip("unstructured")


@pytest.mark.unstructured
@pytest.mark.asyncio
async def test_docx_filedocx():
    p = Path("./tests/processor/docx/demo.docx")
    f = QuivrFile(
        id=uuid4(),
        brain_id=uuid4(),
        original_filename=p.stem,
        path=p,
        file_extension=FileExtension.docx,
        file_sha1="123",
    )
    processor = DOCXProcessor()
    result = await processor.process_file(f)
    assert len(result) > 0


@pytest.mark.unstructured
@pytest.mark.asyncio
async def test_docx_processor_fail(quivr_txt):
    processor = DOCXProcessor()
    with pytest.raises(ValueError):
        await processor.process_file(quivr_txt)
