import json
from pathlib import PosixPath
from uuid import UUID

import pytest
from langchain_core.documents import Document

from quivr_worker.utils import _patch_json


def test_patch_json():
    c = Document(
        page_content="content",
        metadata={
            "id": UUID("a45d9cb8-c05e-41e6-a300-2a54cfdb3f85"),
            "chunk_index": 1,
            "quivr_core_version": "0.0.12",
            "qfile_id": UUID("774ad13d-cde7-40ba-9969-0f71208fc692"),
            "qfile_path": PosixPath(
                "/tmp/pytest-of-amine/pytest-187/test_parse_file0/data.txt"
            ),
            "original_file_name": "data.txt",
            "file_sha1": "124",
            "file_size": 23,
            "date": "20240804",
            "knowledge_id": UUID("774ad13d-cde7-40ba-9969-0f71208fc692"),
            "integration": "",
            "integration_link": "",
            "chunk_size": 6,
            "processor_cls": "TextLoader",
            "splitter": {"chunk_size": 400, "chunk_overlap": 100},
        },
    )

    with pytest.raises(TypeError):
        json.dumps(c.to_json())

    _patch_json()
    assert json.dumps(c.to_json())
