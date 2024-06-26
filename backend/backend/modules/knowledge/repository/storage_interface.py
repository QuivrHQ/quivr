from abc import ABC, abstractmethod


class StorageInterface(ABC):
    @abstractmethod
    def remove_file(self, file_name: str):
        """
        Remove file from storage
        """
        pass
