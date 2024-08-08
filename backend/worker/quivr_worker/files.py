import hashlib
import time
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any
from uuid import UUID

from quivr_api.logger import get_logger
from quivr_core.files.file import FileExtension, QuivrFile

from quivr_worker.utils import get_tmp_name

logger = get_logger(__name__)


def compute_sha1(content: bytes):
    readable_hash = hashlib.sha1(content).hexdigest()
    return readable_hash


@contextmanager
def build_file(
    file_data: bytes,
    knowledge_id: UUID,
    file_name: str,
    original_file_name: str | None = None,
):
    try:
        # FIXME: @chloedia @AmineDiro
        # We should decide if these checks should happen at API level or Worker level
        # These checks should use Knowledge table (where we should store knowledge sha1)
        # file_exists = file_already_exists()
        # file_exists_in_brain = file_already_exists_in_brain(brain.brain_id)
        # TODO(@aminediro) : Maybe use fsspec file to be agnostic to where files are stored :?
        # We are reading the whole file to memory, which doesn't scale
        tmp_name, base_file_name, file_extension = get_tmp_name(file_name)
        tmp_file = NamedTemporaryFile(
            suffix="_" + tmp_name,  # pyright: ignore reportPrivateUsage=none
        )

        file_sha1 = compute_sha1(file_data)
        tmp_file.write(file_data)
        tmp_file.flush()

        file_instance = File(
            knowledge_id=knowledge_id,
            file_name=base_file_name,
            original_file_name=(
                original_file_name if original_file_name else base_file_name
            ),
            tmp_file_path=Path(tmp_file.name),
            file_size=len(file_data),
            file_extension=file_extension,
            file_sha1=file_sha1,
        )
        yield file_instance
    finally:
        # Code to release resource, e.g.:
        tmp_file.close()


class File:
    __slots__ = [
        "id",
        "file_name",
        "tmp_file_path",
        "file_size",
        "file_extension",
        "file_sha1",
        "original_file_name",
    ]

    def __init__(
        self,
        knowledge_id: UUID,
        file_name: str,
        tmp_file_path: Path,
        file_size: int,
        file_extension: str,
        file_sha1: str,
        original_file_name: str,
    ):
        self.id = knowledge_id
        self.file_name = file_name
        self.tmp_file_path = tmp_file_path
        self.file_size = file_size
        self.file_sha1 = file_sha1
        self.file_extension = FileExtension(file_extension)
        self.original_file_name = original_file_name

    def is_empty(self):
        return self.file_size < 1  # pyright: ignore reportPrivateUsage=none

    def to_qfile(self, brain_id: UUID, metadata: dict[str, Any] = {}) -> QuivrFile:
        return QuivrFile(
            id=self.id,
            original_filename=self.file_name,
            path=self.tmp_file_path,
            brain_id=brain_id,
            file_sha1=self.file_sha1,
            file_extension=self.file_extension,
            file_size=self.file_size,
            metadata={
                "date": time.strftime("%Y%m%d"),
                "file_name": self.file_name,
                "original_file_name": self.original_file_name,
                "knowledge_id": self.id,
                **metadata,
            },
        )


def set_file_vectors_ids(self):
    """
    Set the vectors_ids property with the ids of the vectors
    that are associated with the file in the vectors table
    """
    self.vectors_ids = self.supabase_db.get_vectors_by_file_sha1(self.file_sha1).data


def file_already_exists(file: File):
    """
    Check if file already exists in vectors table
    """
    # FIXME: @chloedia @AmineDiro
    # Checking if file exists should be based on the sha1 hash
    # We also return the associated brain(s) here
    return True


# TODO: this is a crazy way to check if file exists
def file_already_exists_in_brain():
    return True