from quivr_api.logger import get_logger
from quivr_api.modules.dependencies import BaseService
from quivr_api.modules.models.entity.model import Model
from quivr_api.modules.models.repository.model import ModelRepository

logger = get_logger(__name__)


class ModelService(BaseService[ModelRepository]):
    repository_cls = ModelRepository

    def __init__(self, repository: ModelRepository):
        self.repository = repository

    async def get_models(self) -> list[Model]:
        logger.info("Getting models")

        models = await self.repository.get_models()

        return models  # type: ignore

    async def get_model(self, model_name: str) -> Model:
        logger.info(f"Getting model {model_name}")

        model = await self.repository.get_model(model_name)

        return model

    async def get_default_model(self) -> Model | None:
        logger.info("Getting default model")

        model = await self.repository.get_default_model()

        return model
