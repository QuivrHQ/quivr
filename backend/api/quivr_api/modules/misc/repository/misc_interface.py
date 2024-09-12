from abc import ABC, abstractmethod




class MiscInterface(ABC):
    @abstractmethod
    def get_health() -> bool:
        pass