import hashlib
import time
from pathlib import Path
from typing import Any
from uuid import UUID

from quivr_api.logger import get_logger
from quivr_core.files.file import FileExtension, QuivrFile

logger = get_logger(__name__)


def compute_sha1(content: bytes):
    readable_hash = hashlib.sha1(content).hexdigest()
    return readable_hash


class File:
    __slots__ = [
        "id",
        "file_name",
        "tmp_file_path",
        "file_size",
        "file_extension",
        "file_sha1",
    ]

    def __init__(
        self,
        knowledge_id: UUID,
        file_name: str,
        tmp_file_path: Path,
        file_size: int,
        file_extension: str,
        file_sha1: str,
    ):
        self.id = knowledge_id
        self.file_name = file_name
        self.tmp_file_path = tmp_file_path
        self.file_size = file_size
        self.file_sha1 = file_sha1
        self.file_extension = FileExtension(file_extension)

    def is_empty(self):
        return self.file_size < 1  # pyright: ignore reportPrivateUsage=none

    def to_qfile(self, brain_id: UUID, metadata: dict[str, Any]) -> QuivrFile:
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
                "original_file_name": self.file_name,
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
