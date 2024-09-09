from abc import ABC, abstractmethod

from quivr_api.modules.models.entity.model import Model


class ModelsInterface(ABC):
    @abstractmethod
    def get_models(self) -> list[Model]:
        """
        Get all models
        """
        pass

    @abstractmethod
    def get_model(self, model_name: str) -> Model:
        """
        Get a model by name
        """
        pass

    @abstractmethod
    def get_default_model(self) -> Model:
        """
        Get the default model
        """
        pass
