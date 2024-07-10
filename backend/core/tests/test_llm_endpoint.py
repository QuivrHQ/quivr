import os

import pytest
from langchain_core.language_models import FakeListChatModel
from langchain_openai import ChatOpenAI
from pydantic.v1.error_wrappers import ValidationError

from quivr_core.config import LLMEndpointConfig
from quivr_core.llm import LLMEndpoint


def test_llm_endpoint_from_config_default():
    del os.environ["OPENAI_API_KEY"]

    with pytest.raises(ValidationError):
        llm = LLMEndpoint.from_config(LLMEndpointConfig())

    # Working default
    config = LLMEndpointConfig(llm_api_key="test")
    llm = LLMEndpoint.from_config(config=config)

    assert llm.supports_func_calling()
    assert isinstance(llm._llm, ChatOpenAI)
    assert llm._llm.model_name in llm.get_config().model


def test_llm_endpoint_constructor():
    llm_endpoint = FakeListChatModel(responses=[])
    llm_endpoint = LLMEndpoint(
        llm=llm_endpoint, llm_config=LLMEndpointConfig(model="test")
    )

    assert not llm_endpoint.supports_func_calling()
