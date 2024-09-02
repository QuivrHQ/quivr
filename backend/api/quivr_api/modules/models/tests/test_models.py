from quivr_api.modules.models.entity.model import Model


def test_model_creation():
    model = Model(name="test-model", price=2, max_input=1000, max_output=500)
    assert model.name == "test-model"
    assert model.price == 2
    assert model.max_input == 1000
    assert model.max_output == 500


def test_model_attributes(test_data):
    model = test_data[0]
    assert hasattr(model, "name")
    assert hasattr(model, "price")
    assert hasattr(model, "max_input")
    assert hasattr(model, "max_output")


def test_model_default_values():
    default_model = Model(name="default-model")
    assert default_model.name == "default-model"
    assert default_model.price == 1
    assert default_model.max_input == 2000
    assert default_model.max_output == 1000


def test_model_comparison():
    model1 = Model(name="model1", price=2, max_input=3000, max_output=1500)
    model2 = Model(name="model2", price=3, max_input=4000, max_output=2000)
    model3 = Model(name="model1", price=2, max_input=3000, max_output=1500)

    assert model1 != model2
    assert model1 == model3
