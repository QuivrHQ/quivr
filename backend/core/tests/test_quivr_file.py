from pathlib import Path
from uuid import uuid4

from quivr_core.files.file import FileExtension, QuivrFile


def test_create_file():
    id = uuid4()
    brain_id = uuid4()
    qfile = QuivrFile(
        id=id,
        brain_id=brain_id,
        original_filename="name",
        path=Path("/tmp/name"),
        file_extension=FileExtension.txt,
        file_sha1="123",
    )

    assert qfile.id == id
    assert qfile.brain_id == brain_id
    assert qfile.original_filename == "name"
    assert qfile.path == Path("/tmp/name")


def test_create_file_add_metadata():
    id = uuid4()
    brain_id = uuid4()
    qfile = QuivrFile(
        id=id,
        brain_id=brain_id,
        original_filename="name",
        path=Path("/tmp/name"),
        file_extension=FileExtension.txt,
        file_sha1="123",
        metadata={"other_id": "id"},
    )

    assert qfile.metadata["other_id"] == "id"
