from pathlib import Path
from uuid import uuid4

import pytest
from quivr_core.files.file import QuivrFile
from quivr_core.storage.local_storage import LocalStorage


@pytest.mark.asyncio
@pytest.mark.parametrize("copy_flag", [True, False])
async def test_upload_file_creates_brain_directory(tmp_path: Path, copy_flag: bool):
    source_path = tmp_path / "source.txt"
    source_path.write_text("stored content")
    brain_id = uuid4()
    file_id = uuid4()
    qfile = QuivrFile(
        id=file_id,
        brain_id=brain_id,
        original_filename=source_path.name,
        path=source_path,
        file_extension=".txt",
        file_sha1="sha1",
    )
    storage = LocalStorage(dir_path=tmp_path / "storage", copy_flag=copy_flag)

    await storage.upload_file(qfile)

    stored_path = tmp_path / "storage" / str(brain_id) / f"{file_id}.txt"
    assert stored_path.read_text() == "stored content"
    assert qfile.path == stored_path
