from pathlib import Path
from uuid import uuid4

import pytest

from quivr_core.files.file import FileExtension, QuivrFile
from quivr_core.processor.implementations.default import UnstructuredPDFProcessor

all_but_pdf = list(filter(lambda ext: ext != ".pdf", list(FileExtension)))


@pytest.mark.asyncio
async def test_unstructured_pdf_processor():
    p = Path("./tests/processor/pdf/sample.pdf")
    f = QuivrFile(
        id=uuid4(),
        brain_id=uuid4(),
        original_filename=p.stem,
        path=p,
        file_extension=FileExtension.pdf,
        file_md5="123",
    )
    processor = UnstructuredPDFProcessor()
    result = await processor.process_file(f)
    assert len(result) > 0


@pytest.mark.parametrize("ext", all_but_pdf)
@pytest.mark.asyncio
async def test_unstructured_pdf_processor_fail(ext):
    p = Path("./tests/processor/pdf/sample.pdf")
    f = QuivrFile(
        id=uuid4(),
        brain_id=uuid4(),
        original_filename=p.stem,
        path=p,
        file_extension=ext,
        file_md5="123",
    )
    processor = UnstructuredPDFProcessor()
    with pytest.raises(ValueError):
        await processor.process_file(f)
