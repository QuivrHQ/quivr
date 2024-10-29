from pathlib import Path
from uuid import uuid4

import pytest
from quivr_core.config import Language, MegaparseConfig, ParserType, StrategyEnum
from quivr_core.files.file import FileExtension, QuivrFile
from quivr_core.processor.implementations.megaparse_processor import MegaparseProcessor
from quivr_core.processor.registry import get_processor_class

all_but_pdf = list(filter(lambda ext: ext != ".pdf", list(FileExtension)))

# unstructured = pytest.importorskip("unstructured")


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
        file_sha1="123",
    )
    megaparse_config = MegaparseConfig(
        method=ParserType.UNSTRUCTURED,
        strategy=StrategyEnum.FAST,
        check_table=False,
        language=Language.ENGLISH,
        parsing_instruction=None,
        model_name="gpt-4o",
    )
    processor = MegaparseProcessor(megaparse_config=megaparse_config)
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
        file_sha1="123",
    )
    processor = MegaparseProcessor()
    with pytest.raises(ValueError):
        await processor.process_file(f)
