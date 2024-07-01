import mmap
import os
from io import BytesIO
from pathlib import Path
from typing import BinaryIO
from uuid import UUID, uuid4

import aiofiles

from quivr_core.storage.storage_base import StorageBase


class QuivrFile:
    __slots__ = ["fd", "filename", "brain_id", "file_size"]

    def __init__(
        self, fd: BinaryIO, filename: str, brain_id: UUID, file_size: int | None = None
    ) -> None:
        self.fd = fd
        self.brain_id = brain_id
        self.filename = filename
        self.file_size = file_size

    @classmethod
    def from_path(cls, path: str):
        fd = os.open(path, os.O_RDONLY)
        file_size = os.stat(path).st_size
        mmapped_file = mmap.mmap(fd, file_size, access=mmap.ACCESS_READ)
        # TODO: parse file_name and brain_id
        file_name = ""
        return cls(
            fd=BytesIO(mmapped_file),
            brain_id=uuid4(),
            filename=file_name,
            file_size=file_size,
        )

    def local_filepath(self) -> str:
        return os.path.join(str(self.brain_id), self.filename)


class LocalStorage(StorageBase):
    def __init__(self, dir_path: Path | None = None):
        if dir_path is None:
            self.dir_path = os.getenv("QUIVR_LOCAL_STORAGE", "~/.cache/quivr/files")
        else:
            self.dir_path = dir_path
        os.makedirs(self.dir_path, exist_ok=True)

    async def upload_file(self, file: QuivrFile, exists_ok: bool = False):
        path = os.path.join(self.dir_path, file.local_filepath())
        if os.path.exists(path) and not exists_ok:
            raise FileExistsError("file already exists")

        async with aiofiles.open(path, "wb") as f:
            await f.write(file.fd.read())

    # TODO:
    async def remove_file(self, file_name: str):
        pass
