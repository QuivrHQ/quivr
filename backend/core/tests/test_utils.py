from quivr_core.utils import model_supports_function_calling


def test_model_supports_function_calling():
    assert model_supports_function_calling("gpt-4") is True
    assert model_supports_function_calling("ollama3") is False
