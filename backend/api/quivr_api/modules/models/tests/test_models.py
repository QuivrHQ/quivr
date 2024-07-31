import pytest
import pytest_asyncio
from quivr_api.modules.models.entity.model import Model


@pytest_asyncio.fixture()
async def sample_models():
    return [
        Model(name="gpt-3.5-turbo", price=1, max_input=4000, max_output=2000),
        Model(name="gpt-4", price=5, max_input=8000, max_output=4000),
    ]


@pytest.mark.asyncio
async def test_model_creation():
    model = Model(name="test-model", price=2, max_input=1000, max_output=500)
    assert model.name == "test-model"
    assert model.price == 2
    assert model.max_input == 1000
    assert model.max_output == 500


@pytest.mark.asyncio
async def test_model_attributes(sample_models):
    model = sample_models[0]
    assert hasattr(model, "name")
    assert hasattr(model, "price")
    assert hasattr(model, "max_input")
    assert hasattr(model, "max_output")


@pytest.mark.asyncio
async def test_model_validation():
    # Test valid model creation
    valid_model = Model(name="valid-model", price=3, max_input=5000, max_output=2500)
    assert valid_model.name == "valid-model"
    assert valid_model.price == 3
    assert valid_model.max_input == 5000
    assert valid_model.max_output == 2500


@pytest.mark.asyncio
async def test_model_default_values():
    default_model = Model(name="default-model")
    assert default_model.name == "default-model"
    assert default_model.price == 1
    assert default_model.max_input == 2000
    assert default_model.max_output == 1000


@pytest.mark.asyncio
async def test_model_comparison():
    model1 = Model(name="model1", price=2, max_input=3000, max_output=1500)
    model2 = Model(name="model2", price=3, max_input=4000, max_output=2000)
    model3 = Model(name="model1", price=2, max_input=3000, max_output=1500)

    assert model1 != model2
    assert model1 == model3


@pytest.mark.asyncio
async def test_model_dict_representation():
    model = Model(name="test-model", price=2, max_input=3000, max_output=1500)
    expected_dict = {
        "name": "test-model",
        "price": 2,
        "max_input": 3000,
        "max_output": 1500,
    }
    assert model.dict() == expected_dict
