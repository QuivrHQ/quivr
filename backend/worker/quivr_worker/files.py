import hashlib
from pathlib import Path
from uuid import UUID

from quivr_api.logger import get_logger
from quivr_api.models.databases.supabase.supabase import SupabaseDB
from quivr_api.modules.brain.service.brain_vector_service import BrainVectorService
from quivr_core.files.file import FileExtension

logger = get_logger(__name__)


def compute_sha1_from_file(file_path: str | Path):
    with open(file_path, "rb") as file:
        bytes = file.read()
        readable_hash = compute_sha1_from_content(bytes)
    return readable_hash


def compute_sha1_from_content(content: bytes):
    readable_hash = hashlib.sha1(content).hexdigest()
    return readable_hash


class File:
    __slots__ = [
        "file_name",
        "tmp_file_path",
        "bytes_content",
        "file_size",
        "file_extension",
        "file_sha1",
    ]

    def __init__(
        self,
        file_name: str,
        tmp_file_path: Path,
        bytes_content: bytes,
        file_size: int,
        file_extension: str,
    ):
        self.file_name = file_name
        self.tmp_file_path = tmp_file_path
        self.bytes_content = bytes_content
        self.file_size = file_size
        self.file_extension = FileExtension[file_extension]
        self.file_sha1 = compute_sha1_from_content(bytes_content)

    def is_empty(self):
        return self.file_size < 1  # pyright: ignore reportPrivateUsage=none


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
def file_already_exists_in_brain(db: SupabaseDB, brain_id: UUID, file_sha1: bytes):
    return True


def link_file_to_brain(self, brain_id):
    self.set_file_vectors_ids()

    if self.vectors_ids is None:
        return

    brain_vector_service = BrainVectorService(brain_id)

    for vector_id in self.vectors_ids:  # pyright: ignore reportPrivateUsage=none
        brain_vector_service.create_brain_vector(vector_id["id"], self.file_sha1)
