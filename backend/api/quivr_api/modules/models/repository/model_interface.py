from abc import ABC, abstractmethod

from quivr_api.modules.models.entity.model import Model


class ModelsInterface(ABC):
    @abstractmethod
    def get_models(self) -> list[Model]:
        """
        Get all models
        """
        pass
