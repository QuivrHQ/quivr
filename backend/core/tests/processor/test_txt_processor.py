from uuid import uuid4

import pytest

from quivr_core.storage.file import FileExtension, QuivrFile


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
    from quivr_core.processor.implementations.default import TikTokenTxtProcessor
    from quivr_core.processor.splitter import SplitterConfig

    tparser = TikTokenTxtProcessor(
        splitter_config=SplitterConfig(chunk_size=20, chunk_overlap=0)
    )
    doc = await tparser.process_file(txt_qfile)
    assert len(doc) > 0
    assert doc[0].page_content == "This is some test data."

    print(doc[0].metadata)
    assert (
        doc[0].metadata.items()
        >= {
            "chunk_index": 0,
            "original_file_name": "data.txt",
            "chunk_size": 6,
            "processor_cls": "TextLoader",
            "splitter": {"chunk_size": 20, "chunk_overlap": 0},
            **txt_qfile.metadata,
        }.items()
    )
