from pathlib import Path
from uuid import uuid4

import pytest
from quivr_core.files.file import FileExtension, QuivrFile

from core.quivr_core.config import Language, MegaparseConfig, ParserType, StrategyEnum
from core.quivr_core.processor.implementations.megaparse_processor import (
    MegaparseProcessor,
)

megaparse = pytest.importorskip("megaparse")


@pytest.mark.megaparse
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
    assert len(result) == 0


@pytest.mark.megaparse
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


@pytest.mark.megaparse
@pytest.mark.asyncio
async def test_epub_processor_fail(quivr_txt):
    megaparse_config = MegaparseConfig(
        method=ParserType.UNSTRUCTURED,
        strategy=StrategyEnum.FAST,
        check_table=False,
        language=Language.ENGLISH,
        parsing_instruction=None,
        model_name="gpt-4o",
    )
    processor = MegaparseProcessor(megaparse_config=megaparse_config)
    with pytest.raises(ValueError):
        await processor.process_file(quivr_txt)
