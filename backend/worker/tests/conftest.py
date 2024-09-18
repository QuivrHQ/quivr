import os
from uuid import uuid4

import pytest
from quivr_worker.files import File


@pytest.fixture
def file_instance(tmp_path) -> File:
    data = "This is some test data."
    temp_file = tmp_path / "data.txt"
    temp_file.write_text(data)
    knowledge_id = uuid4()
    return File(
        knowledge_id=knowledge_id,
        file_sha1="124",
        file_extension=".txt",
        file_name=temp_file.name,
        original_file_name=temp_file.name,
        file_size=len(data),
        tmp_file_path=temp_file.absolute(),
    )


@pytest.fixture
def audio_file(tmp_path) -> File:
    data = os.urandom(128)
    temp_file = tmp_path / "data.mp4"
    temp_file.write_bytes(data)
    knowledge_id = uuid4()
    return File(
        knowledge_id=knowledge_id,
        file_sha1="124",
        file_extension=".mp4",
        file_name=temp_file.name,
        original_file_name="data.mp4",
        file_size=len(data),
        tmp_file_path=temp_file.absolute(),
    )
