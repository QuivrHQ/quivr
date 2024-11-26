from pathlib import Path
from uuid import uuid4

import pytest
from quivr_core.files.file import FileExtension, QuivrFile

megaparse = pytest.importorskip("megaparse")

all_but_pdf = list(filter(lambda ext: ext != ".pdf", list(FileExtension)))


@pytest.mark.megaparse
@pytest.mark.asyncio
async def test_megaparse_pdf_processor():
    from quivr_core.processor.implementations.megaparse_processor import (
        MegaparseProcessor,
    )

    p = Path("./tests/processor/pdf/sample.pdf")
    f = QuivrFile(
        id=uuid4(),
        brain_id=uuid4(),
        original_filename=p.stem,
        path=p,
        file_extension=FileExtension.pdf,
        file_sha1="123",
    )
    processor = MegaparseProcessor()
    result = await processor.process_file(f)
    assert len(result) > 0


@pytest.mark.megaparse
@pytest.mark.parametrize("ext", all_but_pdf)
@pytest.mark.asyncio
async def test_megaparse_pdf_processor_fail(ext):
    from quivr_core.processor.implementations.megaparse_processor import (
        MegaparseProcessor,
    )

    p = Path("./tests/processor/pdf/sample.pdf")
    f = QuivrFile(
        id=uuid4(),
        brain_id=uuid4(),
        original_filename=p.stem,
        path=p,
        file_extension=ext,
        file_sha1="123",
    )
    processor = MegaparseProcessor()
    with pytest.raises(ValueError):
        await processor.process_file(f)
