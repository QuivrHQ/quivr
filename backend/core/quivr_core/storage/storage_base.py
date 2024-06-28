from abc import ABC, abstractmethod

from quivr_core.storage.local_storage import QuivrFile


class StorageBase(ABC):
    @abstractmethod
    async def upload_file(self, file: QuivrFile, exists_ok: bool = False):
        raise Exception("Unimplemented  upload_file method")

    @abstractmethod
    async def remove_file(self, file_name: str):
        raise Exception("Unimplemented remove_file method")
