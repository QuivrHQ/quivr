import hashlib
import time
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any
from uuid import UUID

from quivr_api.logger import get_logger
from quivr_core.files.file import FileExtension, QuivrFile

from quivr_worker.utils.utils import get_tmp_name

logger = get_logger("celery_worker")


def compute_sha1(content: bytes) -> str:
    m = hashlib.sha1()
    m.update(content)
    return m.hexdigest()


@contextmanager
def build_file(
    file_data: bytes,
    knowledge_id: UUID,
    file_name: str,
    original_file_name: str | None = None,
):
    try:
        # TODO(@aminediro) : Maybe use fsspec file to be agnostic to where files are stored :?
        # We are reading the whole file to memory, which doesn't scale
        tmp_name, base_file_name, file_extension = get_tmp_name(file_name)
        tmp_file = NamedTemporaryFile(
            suffix="_" + tmp_name,  # pyright: ignore reportPrivateUsage=none
        )
        tmp_file.write(file_data)
        tmp_file.flush()
        file_sha1 = compute_sha1(file_data)

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
