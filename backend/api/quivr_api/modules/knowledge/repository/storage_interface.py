from abc import ABC, abstractmethod


class StorageInterface(ABC):
    @abstractmethod
    async def upload_file_storage():
        pass

    @abstractmethod
    async def remove_file(self, file_name: str):
        pass
