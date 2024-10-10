from abc import ABC, abstractmethod
from uuid import UUID

from quivr_core.brain.info import StorageInfo
from quivr_core.storage.local_storage import QuivrFile


class StorageBase(ABC):
    """
    Abstract base class for storage systems. All subclasses are required to define certain attributes and implement specific methods for managing files

    Attributes:
        name (str): Name of the storage type.
    """

    name: str

    def __init_subclass__(cls, **kwargs):
        for required in ("name",):
            if not getattr(cls, required):
                raise TypeError(
                    f"Can't instantiate abstract class {cls.__name__} without {required} attribute defined"
                )
        return super().__init_subclass__(**kwargs)

    def __repr__(self) -> str:
        return f"storage_type: {self.name}"

    @abstractmethod
    def nb_files(self) -> int:
        """
        Abstract method to get the number of files in the storage.

        Returns:
            int: The number of files in the storage.

        Raises:
            Exception: If the method is not implemented.
        """
        raise Exception("Unimplemented nb_files method")

    @abstractmethod
    async def get_files(self) -> list[QuivrFile]:
        """
        Abstract asynchronous method to get the files `QuivrFile` in the storage.

        Returns:
            list[QuivrFile]: A list of QuivrFile objects representing the files in the storage.

        Raises:
            Exception: If the method is not implemented.
        """
        raise Exception("Unimplemented get_files method")

    @abstractmethod
    async def upload_file(self, file: QuivrFile, exists_ok: bool = False) -> None:
        """
        Abstract asynchronous method to upload a file to the storage.

        Args:
            file (QuivrFile): The file to upload.
            exists_ok (bool): If True, allows overwriting the file if it already exists. Default is False.

        Raises:
            Exception: If the method is not implemented.
        """
        raise Exception("Unimplemented  upload_file method")

    @abstractmethod
    async def remove_file(self, file_id: UUID) -> None:
        """
        Abstract asynchronous method to remove a file from the storage.

        Args:
            file_id (UUID): The unique identifier of the file to be removed.

        Raises:
            Exception: If the method is not implemented.
        """
        raise Exception("Unimplemented remove_file method")

    def info(self) -> StorageInfo:
        """
        Returns information about the storage, including the storage type and the number of files.

        Returns:
            StorageInfo: An object containing details about the storage.
        """
        return StorageInfo(
            storage_type=self.name,
            n_files=self.nb_files(),
        )
