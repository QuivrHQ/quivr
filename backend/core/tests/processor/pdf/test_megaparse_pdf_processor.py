from pathlib import Path
from uuid import uuid4

import pytest

from quivr_core.files.file import FileExtension, QuivrFile
from quivr_core.processor.implementations.megaparse_processor import MegaparseProcessor
from quivr_core.processor.registry import get_processor_class

all_but_pdf = list(filter(lambda ext: ext != ".pdf", list(FileExtension)))


def test_get_default_processors_megaparse():
    cls = get_processor_class(FileExtension.pdf)
    assert cls == MegaparseProcessor


@pytest.mark.asyncio
async def test_megaparse_pdf_processor():
    p = Path("./tests/processor/pdf/sample.pdf")
    f = QuivrFile(
        id=uuid4(),
        brain_id=uuid4(),
        original_filename=p.stem,
        path=p,
        file_extension=FileExtension.pdf,
        file_md5="123",
    )
    processor = MegaparseProcessor()
    result = await processor.process_file(f)

    assert len(result) > 0


@pytest.mark.parametrize("ext", all_but_pdf)
@pytest.mark.asyncio
async def test_megaparse_fail(ext):
    p = Path("./tests/processor/pdf/sample.pdf")
    f = QuivrFile(
        id=uuid4(),
        brain_id=uuid4(),
        original_filename=p.stem,
        path=p,
        file_extension=ext,
        file_md5="123",
    )
    processor = MegaparseProcessor()
    with pytest.raises(ValueError):
        await processor.process_file(f)
