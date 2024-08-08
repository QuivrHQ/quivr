import pytest

from quivr_api.modules.models.repository.model import ModelRepository
from quivr_api.modules.models.service.model_service import ModelService


@pytest.mark.asyncio
async def test_service_get_chat_models(session):
    repo = ModelRepository(session)
    service = ModelService(repo)
    models = await service.get_models()
    assert len(models) >= 1


@pytest.mark.asyncio
async def test_service_get_non_existing_chat_model(session):
    repo = ModelRepository(session)
    service = ModelService(repo)
    model = await service.get_model("gpt-3.5-turbo")
    assert model is None


@pytest.mark.asyncio
async def test_service_get_existing_chat_model(session):
    repo = ModelRepository(session)
    service = ModelService(repo)
    models = await service.get_models()
    assert len(models) >= 1
    model = models[0]
    model_get = await service.get_model(model.name)
    assert model_get is not None
    assert model_get == model
