from importlib.metadata import version
from uuid import uuid4

import pytest

from quivr_core.processor.splitter import SplitterConfig
from quivr_core.processor.txt_processor import TikTokenTxtProcessor
from quivr_core.storage.file import FileExtension, QuivrFile

# TODO: TIKA server should be set


@pytest.fixture
def txt_qfile(temp_data_file):
    return QuivrFile(
        id=uuid4(),
        brain_id=uuid4(),
        original_filename="data.txt",
        path=temp_data_file,
        file_extension=FileExtension.txt,
        file_md5="hash",
    )


@pytest.mark.base
@pytest.mark.asyncio
async def test_process_txt(txt_qfile):
    tparser = TikTokenTxtProcessor(
        splitter_config=SplitterConfig(chunk_size=20, chunk_overlap=0)
    )
    doc = await tparser.process_file(txt_qfile)
    assert len(doc) > 0
    assert doc[0].page_content == "This is some test data."
    #  assert dict1.items() <= dict2.items()

    assert (
        doc[0].metadata.items()
        >= {
            "chunk_size": len(doc[0].page_content),
            "chunk_overlap": 0,
            "parser_name": tparser.__class__.__name__,
            "quivr_core_version": version("quivr-core"),
            **txt_qfile.metadata,
        }.items()
    )
