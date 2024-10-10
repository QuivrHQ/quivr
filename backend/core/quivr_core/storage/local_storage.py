import os
import shutil
from pathlib import Path
from typing import Self, Set
from uuid import UUID

from quivr_core.brain.serialization import LocalStorageConfig, TransparentStorageConfig
from quivr_core.files.file import QuivrFile
from quivr_core.storage.storage_base import StorageBase


class LocalStorage(StorageBase):
    """
    LocalStorage is a concrete implementation of the `StorageBase` class that
    stores files locally on disk. This class manages file uploads, tracks file
    hashes, and allows retrieval of stored files from a specified directory.

    Attributes:
        name (str): The name of the storage type, set to "local_storage".
        files (list[QuivrFile]): A list of files stored in this local storage.
        hashes (Set[str]): A set of SHA-1 hashes of the uploaded files.
        copy_flag (bool): If `True`, files are copied to the storage directory.
                          If `False`, symbolic links are used instead.
        dir_path (Path): The directory path where files are stored.

    Args:
        dir_path (Path | None): Optional directory path for storing files.
                                Defaults to the environment variable `QUIVR_LOCAL_STORAGE`
                                or `~/.cache/quivr/files`.
        copy_flag (bool): Whether to copy the file or create a symlink.
                          Defaults to `True`.
    """

    name: str = "local_storage"

    def __init__(self, dir_path: Path | None = None, copy_flag: bool = True):
        self.files: list[QuivrFile] = []
        self.hashes: Set[str] = set()
        self.copy_flag = copy_flag

        if dir_path is None:
            self.dir_path = Path(
                os.getenv("QUIVR_LOCAL_STORAGE", "~/.cache/quivr/files")
            )
        else:
            self.dir_path = dir_path
        os.makedirs(self.dir_path, exist_ok=True)

    def _load_files(self) -> None:
        # TODO(@aminediro): load existing files
        pass

    def nb_files(self) -> int:
        return len(self.files)

    def info(self):
        return {"directory_path": self.dir_path, **super().info()}

    async def upload_file(self, file: QuivrFile, exists_ok: bool = False) -> None:
        """
        Uploads a file to the local storage. Copies or creates a symlink based
        on the `copy_flag` attribute. Checks for duplicate file uploads using
        the file's SHA-1 hash.

        Args:
            file (QuivrFile): The file object to upload.
            exists_ok (bool): If `True`, allows overwriting an existing file.
                              Defaults to `False`.

        Raises:
            FileExistsError: If a file with the same SHA-1 hash already exists
                             and `exists_ok` is set to `False`.
        """
        dst_path = os.path.join(
            self.dir_path, str(file.brain_id), f"{file.id}{file.file_extension}"
        )

        if file.file_sha1 in self.hashes and not exists_ok:
            raise FileExistsError(f"file {file.original_filename} already uploaded")

        if self.copy_flag:
            shutil.copy2(file.path, dst_path)
        else:
            os.symlink(file.path, dst_path)

        file.path = Path(dst_path)
        self.files.append(file)
        self.hashes.add(file.file_sha1)

    async def get_files(self) -> list[QuivrFile]:
        """
        Retrieves the list of files stored in the local storage.

        Returns:
            list[QuivrFile]: A list of stored file objects.
        """
        return self.files

    async def remove_file(self, file_id: UUID) -> None:
        """
        Removes a file from the local storage. This method is currently not
        implemented.

        Args:
            file_id (UUID): The unique identifier of the file to remove.

        Raises:
            NotImplementedError: Always raises this error as the method is not yet implemented.
        """
        raise NotImplementedError

    @classmethod
    def load(cls, config: LocalStorageConfig) -> Self:
        """
        Loads the local storage from a configuration object. This method
        initializes the storage directory and populates it with deserialized
        files from the configuration.

        Args:
            config (LocalStorageConfig): Configuration object containing the
                                         storage path and serialized file data.

        Returns:
            LocalStorage: An instance of `LocalStorage` with files loaded
                          from the configuration.
        """
        tstorage = cls(dir_path=config.storage_path)
        tstorage.files = [QuivrFile.deserialize(f) for f in config.files.values()]
        return tstorage


class TransparentStorage(StorageBase):
    """Transparent Storage."""

    name: str = "transparent_storage"

    def __init__(self):
        self.id_files = {}

    async def upload_file(self, file: QuivrFile, exists_ok: bool = False) -> None:
        self.id_files[file.id] = file

    def nb_files(self) -> int:
        return len(self.id_files)

    async def remove_file(self, file_id: UUID) -> None:
        raise NotImplementedError

    async def get_files(self) -> list[QuivrFile]:
        return list(self.id_files.values())

    @classmethod
    def load(cls, config: TransparentStorageConfig) -> Self:
        tstorage = cls()
        tstorage.id_files = {
            i: QuivrFile.deserialize(f) for i, f in config.files.items()
        }
        return tstorage
