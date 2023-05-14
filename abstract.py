from abc import ABC, abstractmethod

class VectorStoreInterface(ABC):
    @abstractmethod
    def select(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        pass