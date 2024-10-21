import pytest
from quivr_core.processor.implementations.tika_processor import TikaProcessor

# TODO: TIKA server should be set


@pytest.mark.tika
@pytest.mark.asyncio
async def test_process_file(quivr_pdf):
    tparser = TikaProcessor()
    doc = await tparser.process_file(quivr_pdf)
    assert len(doc) > 0
    assert doc[0].page_content.strip("\n") == "Dummy PDF download"


@pytest.mark.tika
@pytest.mark.asyncio
async def test_send_parse_tika_exception(quivr_pdf):
    # TODO: Mock correct tika for retries
    tparser = TikaProcessor(tika_url="test.test")
    with pytest.raises(RuntimeError):
        doc = await tparser.process_file(quivr_pdf)
        assert len(doc) > 0
        assert doc[0].page_content.strip("\n") == "Dummy PDF download"
